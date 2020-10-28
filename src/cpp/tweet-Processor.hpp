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

    // remove a cascade from a the queue
    // and then send a kafka message
    /// the function to send a kafka message should be added in the class Cascade!
    void remove_cascade(ref cascade_ptr);

    virtual ~Processor() {};

  };


  struct ProcessorsHandler {
    // a map containing all the processors (every processor is associated with a source)
    std::map<source::idf, Processor> processors;
    // we add the terminated time in the attributes of the ProcessorsHandler
    // in order to use it in checking if we should send the kafka message !
    std::size_t terminated_cascade;

    ProcessorsHandler() = default;
    ProcessorsHandler(std::size_t t_c) : terminated_cascade(t_c) {};
    //ProcessorsHandler(const Processor& pr) = default;
    virtual ~ProcessorsHandler() {};

    // This adds a module to the cursus... or changes its coefficient.
    void operator+=(const std::tuple<source::idf, cascade::idf, tweet&>& processor) {
      // boolean value allows us to check of the cascade already exists in
      // the queue
      bool cascade_exists = false;
        // If the module does not exist yet, we create it.
        // The arguments following the key of try_emplace fit the ones of a Module constructor.
      auto [it, is_newly_created] = processors.try_emplace(std::get<0>(processor),
                                                           std::get<1>(processor),
                                                           std::get<2>(processor));

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
              // params.topic.terminated=1800
              if (std::get<2>(processor).time - c->latest_time > terminated_cascade) {
                std::cout << "   cascade terminated - send kafka msg !  - TO BE REMOVED "
                          << terminated_cascade << std::endl;
                /// we can print the content of the cascade using the operator <<
                /// note that we should put *c and not just c.
                /// cout :
                //std::cout << *c << std::endl;

                // to be added : a producer to a topic (let's call it "cascade")
                // and send the messages

                // cascade to be sent in a kafka message
                // remove the cascade from the processor
                // check if the the processor is eampty or not
              } else {
                c->latest_time = std::get<2>(processor).time;
                c->twts.push_back(std::get<2>(processor));
              }

            }
          }
          if (! cascade_exists) {
            // push to queue
            auto r = cascade_ptr(std::get<1>(processor), std::get<2>(processor));
            r->location = it->second.queue.push(r);
            // using this print, we can see that when a new cascade is
            // created, the size of the queue increases by one
            // see the condition followed by the print at the end of this function
            ///if (std::get<0>(processor) == 1) std::cout << "cascade created !" << std::endl;
          }
          // set the boolean value to false
          cascade_exists = false;
        }
      }

      // prints to check for a given source the effect of the creation of cascade on the processor
      ///if (std::get<0>(processor) == 1) std::cout << "source: " << std::get<0>(processor)
      ///                                 << " - size:"  << it->second.queue.size() << std::endl;

    }

    // This removes a processor
    void operator-=(const source::idf& s) {
      if(auto it = processors.find(s); it != processors.end())
        processors.erase(it);
    }

  };

}
