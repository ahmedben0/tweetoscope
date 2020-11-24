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

    os << "\"{\'key\' : "        << c.key         << " , "
       << "\'source_id\' : "   << c.source_id   << " , "
       << "\'msg\' : "         << c.msg         << " , "
       << "\'latest_time\' : " << c.latest_time << " , "
       << "\'list_retweets\' : [";
    // the information related to the retweets are stored
    // in a list of dictionnary
    for(auto ptr_t = c.twts.begin(); ptr_t != c.twts.end(); ++ptr_t){
      // the information to keep from a retweet are :
      // the time, the magnitude and the info
      os << "{\'time\': "     << ptr_t->time      << " , "
         << "\'magnitude\': " << ptr_t->magnitude << " , "
         << "\'info\': \'"    << ptr_t->info      << "\'}";
      // we add a comma at the end of every retweet but the last one
      if (ptr_t != c.twts.end()-1) os << ",";
    }

    os << "]}\"";
    return os;
  }

  std::string msg_cascade_series(const Cascade& c, cascade::idf obs) {
    // Key = None Value = { 'type' : 'serie', 'cid': 'tw23981', 'msg' : 'blah blah', 'T_obs': 600, 'tweets': [ (t1, mag1), (t2,mag2), ... ] }
    std::ostringstream os;

    os << "{\"type\" : "  << "\"serie\""  << " , "
       << "\"cid\": "    << c.key        << " , "
       << "\"msg\" : \""    << c.msg        << "\" , "
       << "\"T_obs\" : "  << obs          << " , "  // to be changed : T_obs = obs (600, 1200 ... )
       << "\"tweets\" : [";
    // the information related to the retweets are stored
    // in a list of dictionnary
    for(auto ptr_t = c.twts.begin(); ptr_t != c.twts.end(); ++ptr_t){
      // the information to keep from a retweet are :
      // the time, the magnitude and the info
      os << "(" << ptr_t->time << ", " << ptr_t->magnitude << ")";
      // we add a comma at the end of every retweet but the last one
      if (ptr_t != c.twts.end()-1) os << ",";
    }

    os << "]}";
    return os.str();
  }


  std::string msg_cascade_properties(const Cascade& c) {
    // Key = 300  Value = { 'type' : 'size', 'cid': 'tw23981', 'n_tot': 127, 't_end': 4329 }
    std::ostringstream os;

    os << "{\"type\" : "  << "\"size\""    << " , "
       << "\"cid\" : "    << c.key         << " , "
       << "\"n_tot\" : "  << c.twts.size() << " , "
       << "\"t_end\" : "  << c.latest_time << "}";

    return os.str();
  }

  bool element_ref_comparator::operator()(ref op1, ref op2) const {
    return *op1 < *op2;
  }


  void send_kafka_msg(ref c_ptr, const ProcessorsHandler& pr, cascade::idf obs, char c_type) {
    // c_type will allow us to determin if we will send the message
    // on the cascade_series or the cascade_properties
    // possible values : 's', 'p'

    // kafka producer !
    cppkafka::Configuration config_c {
      {"metadata.broker.list", pr.params_.kafka.brokers},
      {"log.connection.close", false }
    };

    cppkafka::Producer  producer_c(config_c);

    if (c_type == 's') {
      cppkafka::MessageBuilder builder_c {pr.params_.topic.out_series};

      auto key = std::to_string(NULL);
      builder_c.key(key);
      std::ostringstream ostr;
      ostr.str(msg_cascade_series(*c_ptr, obs));
      auto msg = ostr.str();
      builder_c.payload(msg);
      producer_c.produce(builder_c);
    }

    if (c_type == 'p') {
      cppkafka::MessageBuilder builder_c {pr.params_.topic.out_properties};

      auto key = std::to_string(obs);
      builder_c.key(key);
      std::ostringstream ostr;
      ostr.str(msg_cascade_properties(*c_ptr));
      auto msg = ostr.str();
      builder_c.payload(msg);
      producer_c.produce(builder_c);
    }
  }

}
