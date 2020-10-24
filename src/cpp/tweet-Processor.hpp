// add includes

namespace tweetoscope {

  struct Processor {
    source::idf src;
    std::vector<tweet> tweets;
    // shall we add a list for all the tweets for a given processor ?

    Processor()                    = default;
    //Processor(const Processor& pr) = default;
    Processor(source::idf s, tweet& t) : src(s) {
      tweets.push_back(t);
    };
    virtual ~Processor() {};

    // add functions to handle a given tweet
  };

  struct ProcessorsHandler {
    std::map<source::idf, Processor> processors;

    ProcessorsHandler()                    = default;
    //ProcessorsHandler(const Processor& pr) = default;
    virtual ~ProcessorsHandler() {};

    // This adds a module to the cursus... or changes its coefficient.
    void operator+=(const std::tuple<source::idf, source::idf, tweet&>& processor) {
        // If the module does not exist yet, we create it.
        // The arguments following the key of try_emplace fit the ones of a Module constructor.
      auto [it, is_newly_created] = processors.try_emplace(std::get<0>(processor), std::get<1>(processor), std::get<2>(processor));
      if(is_newly_created)
        std::cout << "New Process created " << std::endl;
      else {
        it->second.src = std::get<1>(processor);
        it->second.tweets.push_back(std::get<2>(processor));

        // print the size of the vector "tweet" to check that the tweet is added
        std::cout << "source id : " << it->second.src
                  << " - # of tweets in this source : " << it->second.tweets.size()
                  << std::endl;
      }
    }

    // This removes a processor
    void operator-=(const source::idf& s) {
      if(auto it = processors.find(s); it != processors.end())
        processors.erase(it);
    }

  };

}
