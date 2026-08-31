#include "hiddenlayer.hpp"
#include "layer.hpp"
#include "neuron.hpp"
#include "thresholdneuron.hpp"

HiddenLayer::HiddenLayer(vector<float> input, int nNeurons) : Layer(input,nNeurons) {
  ThresholdNeuron *x = new ThresholdNeuron(input);
  neurons.push_back(x);
}


