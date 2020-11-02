#pragma once

#include "tweet-Cascade.hpp"


namespace tweetoscope {

  bool Cascade::operator<(const Cascade& other) const {
    // decreasing order <
    return latest_time < other.latest_time;
  }


  std::ostream& operator<<(std::ostream& os, const Cascade& c) {
    // the operator << will allow us to (1) print the cascade
    // and (2 - most importantly) send the cascade as a kafka message

    os << "{\"key\" : "        << c.key         << " , "
       << "\"source_id\" : "   << c.source_id   << " , "
       << "\"msg\" : "         << c.msg         << " , "
       << "\"latest_time\" : " << c.latest_time << " , "
       << "\"list_retweets\" : [";
    // the information related to the retweets are stored
    // in a list of dictionnary
    for(auto ptr_t = c.twts.begin(); ptr_t != c.twts.end(); ++ptr_t){
      // the information to keep from a retweet are :
      // the time, the magnitude and the info
      os << "{\"time\": "     << ptr_t->time      << " , "
         << "\"magnitude\": " << ptr_t->magnitude << " , "
         << "\"info\": \""    << ptr_t->info      << "\"}";
      // we add a comma at the end of every retweet but the last one
      if (ptr_t != c.twts.end()-1) os << ",";
    }

    os << "]}";
    return os;
  }


  bool element_ref_comparator::operator()(ref op1, ref op2) const {
    return *op1 < *op2;
  }

  // kafka producer !
  cppkafka::Configuration config_c {
    // we should modify the config file !
	  {"metadata.broker.list", "localhost:9092" },
	  {"log.connection.close", false }
	};

  // same here : name of the topic should be in config file as well
  cppkafka::MessageBuilder builder_c {"cascades"};
	cppkafka::Producer       producer_c(config_c);

  void send_kafka_msg(ref c_ptr) {
    // send the cascade in a kafka message

    auto key = std::to_string(c_ptr->key);
    builder_c.key(key);
    std::ostringstream ostr;
    ostr << *c_ptr;
    auto msg = ostr.str();
    builder_c.payload(msg);
    producer_c.produce(builder_c);

    std::cout << *c_ptr << std::endl;
  }


}
