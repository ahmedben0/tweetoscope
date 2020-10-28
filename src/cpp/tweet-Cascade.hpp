#pragma once

#include <memory>
#include <boost/heap/binomial_heap.hpp>
#include <iostream>
#include <iomanip>
#include <string>
#include <vector>


namespace tweetoscope {

  struct Cascade;
  // a tweet and all retweets it triggered, build up what is hereafter called a cascade

  using ref = std::shared_ptr<Cascade>;

  // This is the comparison functor for boost queues.
  struct element_ref_comparator {
    bool operator()(ref op1, ref op2) const; // Defined later.
  };

  // We define our queue type.
  using priority_queue = boost::heap::binomial_heap<ref,
                            boost::heap::compare<element_ref_comparator>>;

  // define the Cascade class/structure
  struct Cascade {
    // cascades in the queues are sorted according to
    // the date of their last tweet, in a decreasing odrer
    // add more attributes
    cascade::idf key;         // the id of the original tweet
    source::idf source_id;    // the id if the source of the tweet
    std::string msg;          // msg of the tweet
    timestamp latest_time;    // the time of the newest retweet
    std::vector<tweet> twts;  // a vector containing all the retweets

    priority_queue::handle_type location; // This is "where" the element
                                          // is in the queue. This is
                                          // needed when we change the
                                          // priority.


    bool operator<(const Cascade& other) const {
      // decreasing order <
      return latest_time < other.latest_time;
    }

    // add more constructors
    Cascade() = default;
    Cascade(cascade::idf key, const tweet& t) : key(key),
                                                source_id(t.source),
                                                msg(t.msg),
                                                latest_time(t.time)
    {
      twts.push_back(t);
    };

    virtual ~Cascade() {};

  };


  bool element_ref_comparator::operator()(ref op1, ref op2) const {
    return *op1 < *op2;
  }

  ref cascade_ptr(cascade::idf key, const tweet& t) {
    return std::make_shared<Cascade>(key, t);
  }

}
