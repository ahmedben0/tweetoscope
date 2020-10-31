#pragma once

#include "tweet-Processor.hpp"

namespace tweetoscope {

  Processor::Processor(cascade::idf key, tweet& t) {
    auto r = cascade_ptr(key, t);
    r->location = queue.push(r);

    // partial_cascade.insert(std::make_pair(t.time, ));

    // a shared pointer IS a weak pointer
    symbol_table.insert(std::make_pair(key, r));
  }


  void ProcessorsHandler::operator-=(const source::idf& s) {
    if(auto it = processors.find(s); it != processors.end())
      processors.erase(it);
  }


  void ProcessorsHandler::operator+=(const std::tuple<source::idf, cascade::idf, tweet&>& processor) {
    // boolean value allows us to check of the cascade already exists in the queue
    bool cascade_exists = false;
      // If the module does not exist yet, we create it.
      // The arguments following the key of try_emplace fit the ones of a Module constructor.
    auto [it, is_newly_created] = processors.try_emplace(std::get<0>(processor),
                                                         std::get<1>(processor),
                                                         std::get<2>(processor));

    if(! is_newly_created) {
      // check for the processor with the same source
      // as the tweet for the cascade
      if(auto ptr_p = processors.find(std::get<0>(processor)); ptr_p != processors.end()) {
        // we have the address of the corresponding source
        // we will loop over this process and see if we already have the cascade
        for(const auto& c : ptr_p->second.queue) {
          // 2 cascades are equals if they have the same key
          if (c->key == std::get<1>(processor)) {
            cascade_exists = true;
            // params.topic.terminated=1800
            if (std::get<2>(processor).time - c->latest_time > terminated_cascade) {
              // send the cascade in a kafka message
              send_kafka_msg(c);

              // remove a cascade from a the queue
              if (! ptr_p->second.queue.empty()) {
                ptr_p->second.queue.erase(c->location);

                // we just deleted an element from the list
                // it makes sense then to check if the queue is empty
                // and delete it if it is the case
                if (ptr_p->second.queue.empty()){
                  this->operator-=(c->source_id);
                }
                // cascade found, no need to continue the loop
                break;
              }

              // check if the processor is emty and delete it it is the case
              if (ptr_p->second.queue.empty()){
                this->operator-=(c->source_id);
              }

              // add the tweet to the vector of tweets in the cascade
            } else {
              c->latest_time = std::get<2>(processor).time;
              c->twts.push_back(std::get<2>(processor));
            }

          }
        }
        // in case the cascade does not exist
        if (! cascade_exists) {
          // push to queue
          auto r = cascade_ptr(std::get<1>(processor), std::get<2>(processor));
          r->location = it->second.queue.push(r);
          it->second.queue.update(r->location);
          it->second.symbol_table.insert(std::make_pair(std::get<1>(processor), r));

        }
        // set the boolean value to false
        cascade_exists = false;
      }
    }

  }




}
