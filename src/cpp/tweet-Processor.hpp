#pragma once

#include "tweet-Cascade.hpp"

namespace tweetoscope {

  struct Processor {

    // queue
    priority_queue queue;
    // partial cascade
    std::map<timestamp, std::queue<ref>> partial_cascade;
    // symbol table
    std::map<cascade::idf, ref_w> symbol_table;

    Processor() = default;
    Processor(cascade::idf key, tweet& t);
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

    virtual ~ProcessorsHandler() {};

    // This removes a processor
    void operator-=(const source::idf& s);

    // This adds a module to the cursus... or changes its coefficient.
    void operator+=(const std::tuple<source::idf, cascade::idf, tweet&>& processor);

  };

}
