#include <iostream>
#include <iomanip>
#include <fstream>
#include <queue>
#include <thread>
#include <atomic>
#include <stdexcept>

#include <gaml.hpp>

#include "tweetoscopeCollectorParams.hpp"
#include <iterator>
#include <cppkafka/cppkafka.h>
#include "tweet-collector.hpp"

#include <sstream>
#include <map>
#include <vector>
#include <tuple>

#include "tweet-Processor.cpp"
#include "tweet-Cascade.cpp"

#include <spdlog/spdlog.h>
#include <spdlog/sinks/stdout_color_sinks.h>

int main(int argc, char* argv[]) {

  std::shared_ptr<spdlog::logger> stdout_logger = spdlog::stdout_color_mt("stdout");
  spdlog::set_default_logger(stdout_logger);

  // disable logs
  //spdlog::set_level(spdlog::level::off);

  // debug mode
  //spdlog::set_level(spdlog::level::debug);


  if(argc != 2) {
    std::cout << "Usage : " << argv[0] << " <config-filename>" << std::endl;
    return 0;
  }


  tweetoscope::params::collector params(argv[1]);
  std::cout << std::endl
        << "Parameters : " << std::endl
        << "----------"    << std::endl
        << std::endl
        << params << std::endl
        << std::endl;



  // Create the kafka consumer
	cppkafka::Configuration config {
	  {"metadata.broker.list", params.kafka.brokers},
    { "auto.offset.reset", "earliest" },
	  {"log.connection.close", false },
    // a groud id is mandatory to avoid errors related to the subscription to the topic
    {"group.id","mygroup"}
	};

	cppkafka::Consumer consumer(config);

  // Subscribe to the topic
  consumer.subscribe({params.topic.in});

  // the class ProcessorsHandler takes care of the Processor bsed on the source
  // tweetoscope::ProcessorsHandler processors(params.times.terminated);
  tweetoscope::ProcessorsHandler processors(argv[1]);

  while(true) {
    auto msg = consumer.poll();
    if( msg && ! msg.get_error() ) {
      // std::cout << i++ << std::endl;
      tweetoscope::tweet twt;
      auto key = tweetoscope::cascade::idf(std::stoi(msg.get_key()));
      auto istr = std::istringstream(std::string(msg.get_payload()));
      istr >> twt;

      spdlog::debug("[{}] new tweet received : key : {} - value : {}", params.topic.in, key, istr.str());
      // we use the maps to handle the processors
      processors += {twt.source, key, twt};
      consumer.commit(msg);
    }
}

  return 0;
}
