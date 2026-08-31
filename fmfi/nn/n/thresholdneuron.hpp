#ifndef __THRESHOLDNEURON_HPP_
#define __THRESHOLDNEURON_HPP_

#include "neuron.hpp"

class ThresholdNeuron : public Neuron {
  public:
    ThresholdNeuron(vector<float> input); 
    float processInput(vector<float> input, int errorcount);
};


#endif __TRESHOLDNEURON_HPP_

 