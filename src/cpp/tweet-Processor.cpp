#pragma once

#include "tweet-Processor.hpp"

namespace tweetoscope {

  /////////////////
  /// Processor ///
  /////////////////

  Processor::Processor(cascade::idf key, tweet& t, params::collector p) : params_(p) {
    auto r = cascade_ptr(key, t);
    r->location = queue.push(r);

    for (auto obs : p.times.observation) {
      partial_cascade.insert({obs, {}});
      // add the cascade to all the observations !
      partial_cascade[obs].push(r);
    }

    // a shared pointer IS a weak pointer
    symbol_table.insert(std::make_pair(key, r));
  }

  /////////////////////////
  /// ProcessorsHandler ///
  /////////////////////////

  void ProcessorsHandler::operator-=(const source::idf& s) {
    if(auto it = processors.find(s); it != processors.end())
      processors.erase(it);
  }


  void ProcessorsHandler::operator+=(const std::tuple<source::idf, cascade::idf, tweet&>& processor) {
    auto [ptr_p, is_pr_newly_created] = processors.try_emplace(std::get<0>(processor),
                                                               std::get<1>(processor),
                                                               std::get<2>(processor),
                                                               this->params_);

    if (!is_pr_newly_created) {

      auto c_ptr = cascade_ptr(std::get<1>(processor), std::get<2>(processor));
      auto [it_s, is_symbol_created] = ptr_p->second.symbol_table.insert(std::make_pair(std::get<1>(processor), c_ptr));


      //////////////////
      /// priority queue
      //////////////////
      while(!ptr_p->second.queue.empty() && this->params_.times.terminated \
               < std::get<2>(processor).time - ptr_p->second.queue.top()->latest_time) {

        auto r = ptr_p->second.queue.top();
        // send the kafka : topic = cascade_series
        std::cout << "[cascade_series] Key = None  Values = " << msg_cascade_series(*r) << std::endl;
        send_kafka_msg(r, *this, r->key);
        ptr_p->second.queue.pop();
      }

      if (is_symbol_created) c_ptr->location = ptr_p->second.queue.push(c_ptr);

      ////////////////////
      /// partial cascades
      ////////////////////
      for(auto& [obs, cascades]: ptr_p->second.partial_cascade){
        while(!cascades.empty()) {
          if (auto sp_r = cascades.front().lock()) {
            cascades.pop();
            if (std::get<2>(processor).time - sp_r->first_time > obs) {
              // send the kafka : topic = cascade_properties
              std::cout << "[cascade_properties] Key = " << obs  << "  Values = " <<  msg_cascade_properties(*sp_r) << std::endl;
              send_kafka_msg(sp_r, *this, obs);
            } //else break;
          } else cascades.pop();
        }
        // new created cascade, so it should added to all the partial cascades
        if(is_symbol_created) cascades.push(c_ptr);
      }

      ////////////////
      /// update queue
      ////////////////
      if(auto sp = it_s->second.lock()) {
        sp->latest_time = std::get<2>(processor).time;
        if (!is_symbol_created) sp->twts.push_back(std::get<2>(processor)); // push the tweets to the cascade
        ptr_p->second.queue.update(sp->location);
      }
    }
  }



}
