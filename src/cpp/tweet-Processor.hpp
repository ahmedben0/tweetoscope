// add includes

// add queue to the Processor
#pragma once

#include "tweet-Cascade.hpp"

namespace tweetoscope {

  struct Processor {

    // A first attribute of your processor will
    // be a queue that stores the cascade you handle.

    // queue
    priority_queue queue;


    Processor() = default;
    Processor(cascade::idf key, tweet& t) {
      auto r = cascade_ptr(key, t);
      r->location = queue.push(r);
    };

    virtual ~Processor() {};

    // add functions to handle a given tweet
  };




  struct ProcessorsHandler {
    std::map<source::idf, Processor> processors;

    ProcessorsHandler() = default;
    //ProcessorsHandler(const Processor& pr) = default;
    virtual ~ProcessorsHandler() {};

    // This adds a module to the cursus... or changes its coefficient.
    void operator+=(const std::tuple<source::idf, cascade::idf, tweet&>& processor) {
      // boolean value allows us to check of the cascade already exists in
      // the queue
      bool cascade_exists = false;
        // If the module does not exist yet, we create it.
        // The arguments following the key of try_emplace fit the ones of a Module constructor.
      auto [it, is_newly_created] = processors.try_emplace(std::get<0>(processor), std::get<1>(processor), std::get<2>(processor));

      if(is_newly_created) {
        // tweet and retweets are from the same source.
        // so if a new processor is created, that means
        // that a new cascade should also so created !
        std::cout << "New Process created - source : " << std::get<0>(processor) << std::endl;
        // the cascade is created from the contructor of the Processor class

      }
      else {
        // check for the processor with the same source
        // as the tweet for the cascade
        if(auto ptr_p = processors.find(std::get<0>(processor)); ptr_p != processors.end()) {
          // we have the address of the corresponding source
          // we will loop over this process and see if we already have the cascade
          for(const auto& c : ptr_p->second.queue) {
            // 2 cascades are equals if they have the same key
            if (c->key == std::get<1>(processor)) {
              cascade_exists = true;
              c->latest_time = std::get<2>(processor).time;
              c->twts.push_back(std::get<2>(processor));

            }
          }
          if (! cascade_exists) {
            // push to queue
            auto r = cascade_ptr(std::get<1>(processor), std::get<2>(processor));
            r->location = it->second.queue.push(r);
            // using this print, we can see that when a new cascade is
            // created, the size of the queue increases by one
            // see the condition followed by the print at the end of this function
            if (std::get<0>(processor) == 1) std::cout << "cascade created !" << std::endl;
          }
          // set the boolean value to false
          cascade_exists = false;
        }
      }

      // prints to check for a given source the effect of the creation of cascade on the processor
      if (std::get<0>(processor) == 1) std::cout << "source: " << std::get<0>(processor) << " - size:"  << it->second.queue.size() << std::endl;

    }

    // This removes a processor
    void operator-=(const source::idf& s) {
      if(auto it = processors.find(s); it != processors.end())
        processors.erase(it);
    }

  };

}
