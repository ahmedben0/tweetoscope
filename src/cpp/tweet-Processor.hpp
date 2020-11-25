#pragma once

#include "tweet-Cascade.hpp"

namespace tweetoscope {

  struct Processor {

    // parameters from the config file
    params::collector params_;
    // queue
    priority_queue queue;
    // partial cascade
    std::map<timestamp, std::queue<ref_w>> partial_cascade;
    // symbol table
    std::map<cascade::idf, ref_w> symbol_table;

    Processor() = default;
    Processor(cascade::idf key, tweet& t, params::collector p);
    virtual ~Processor() {};

  };


  struct ProcessorsHandler {
    // a map containing all the processors (every processor is associated with a source)
    std::map<source::idf, Processor> processors;

    // parameters from the config file
    params::collector params_;

    cppkafka::Producer  producer_c;


    ProcessorsHandler() = delete;
    ProcessorsHandler(const std::string& config_filename) : producer_c({
      {"metadata.broker.list", params::collector(config_filename).kafka.brokers},
      {"log.connection.close", false }
      })  {
        params_ = params::collector(config_filename);
      };

    virtual ~ProcessorsHandler() {};

    // This removes a processor
    void operator-=(const source::idf& s);

    void operator+=(const std::tuple<source::idf, cascade::idf, tweet&>& processor);

    void update_processor(Processor& pr, ref c);

  };

}
