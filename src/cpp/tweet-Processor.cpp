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

      // delete terminated cascade
      while(!ptr_p->second.queue.empty() && this->params_.times.terminated \
               < std::get<2>(processor).time - ptr_p->second.queue.top()->latest_time) {  // first or latest ?

        ref r = ptr_p->second.queue.top();
        // send the kafka : topic = cascade_series
        std::cout << "Key = None  Values = " << msg_cascade_series(*r) << std::endl;
        send_kafka_msg(r, *this, r->key);
        ptr_p->second.queue.pop();
      }

      auto c_ptr = cascade_ptr(std::get<1>(processor), std::get<2>(processor));
      auto [it_s, is_symbol_created] = ptr_p->second.symbol_table.insert(std::make_pair(std::get<1>(processor), c_ptr));



      /*  // change this part  !!!!
      if (is_symbol_created) ptr_p->second.queue.push(c_ptr);

      for(auto& [obs, cascades]: ptr_p->second.partial_cascade){

        while(!cascades.empty() && std::get<2>(processor).time - cascades.front()->first_time > obs) {
          ref r = cascades.front();
          send_kafka_msg(r, *this, obs);
          std::cout << "Key = " << obs  << "  Values = " <<  msg_cascade_properties(*r) << std::endl;
          cascades.pop();
        }

        // new created cascade, so it should added to all the partial cascades
        if(is_symbol_created) cascades.push(c_ptr);
      }

      if(auto sp = it_s->second.lock()) {
        sp->latest_time = std::get<2>(processor).time;
        ptr_p->second.queue.update(sp->location);
      }
      */ //


      // /*
      if(auto sp = it_s->second.lock()) {
      // the cascade has just been created, no need then to change the latest_time attribute
        sp->latest_time = std::get<2>(processor).time;
        this->update_processor(ptr_p->second, sp);
      }
      // */

    }
  }


  void ProcessorsHandler::update_processor(Processor& pr, ref c) {
    c->location = pr.queue.push(c);
    pr.queue.update(c->location);

    auto end = pr.params_.times.observation.end();
    bool remove_shared_ptr = false;

    for (auto obs : pr.params_.times.observation) {
      //std::cout << c->latest_time << " --- " << c->first_time << std::endl;
      if (c->latest_time - c->first_time < obs) pr.partial_cascade[obs].push(c);
      else {
        if (obs == *end) remove_shared_ptr = true;
        std::cout << "Key = " << obs  << "  Values = " <<  msg_cascade_properties(*c) << std::endl;
        send_kafka_msg(c, *this, obs);
        // remove the cascade from this partial cascade !
        if (pr.partial_cascade[obs].size()) pr.partial_cascade[obs].pop();
      }
    }

    if (remove_shared_ptr) pr.symbol_table.erase(c->key);
  }


}
