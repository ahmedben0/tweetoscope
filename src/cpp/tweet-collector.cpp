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

#include "tweet-Processor.hpp"
#include "tweet-Cascade.hpp"

int main(int argc, char* argv[]) {


  if(argc != 2) {
    std::cout << "Usage : " << argv[0] << " <config-filename>" << std::endl;
    return 0;
  }

  // random seed initialization
  //std::random_device rd;
  //std::mt19937 gen(rd());

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
  tweetoscope::ProcessorsHandler processors(params.times.terminated);


  while(true) {
    auto msg = consumer.poll();
    if( msg && ! msg.get_error() ) {
       tweetoscope::tweet twt;
       auto key = tweetoscope::cascade::idf(std::stoi(msg.get_key()));
       auto istr = std::istringstream(std::string(msg.get_payload()));
       istr >> twt;

       // simple prints to show that the collector works

       // all the information is in the variable twt
       // we can access easily to all the parts of the msg


       /*
       std::cout << "key: "       << key           << " - "
                 << "type: "      << twt.type      << " - "
                 << "msg: "       << twt.msg       << " - "
                 << "time: "      << twt.time      << " - "
                 << "magnitude: " << twt.magnitude << " - "
                 << "source: "    << twt.source    << " - "
                 << "info: "      << twt.info
                 << std::endl;
       */


       // we use the maps to handle the processors
       processors += {twt.source, key, twt};

       consumer.commit(msg);

    }
}

  return 0;
}
