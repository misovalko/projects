#include "layer.hpp"
#include "neuron.hpp"

Layer::Layer(vector<float> input, int nNeurons) {
 this->input=input;
 for(int i=0;i<nNeurons;i++)
  neurons.push_back(new Neuron(input));
}

vector<float> Layer::processInput(vector<float> input, int errorcount) {
  this->input=input;
  output.clear();
  for(unsigned i=0;i<neurons.size();i++)
    output.push_back(neurons[i]->processInput(input,errorcount));
  return output;
}


void Layer::randWeights() {
  for(unsigned i=0;i<neurons.size();i++)
    neurons[i]->randWeights();
}


void Layer::changeWeights(float alpha, float momentum) {
  for(unsigned i=0;i<neurons.size();i++)
    neurons[i]->changeWeights(alpha,momentum,delta[i]);
}

Layer::~Layer() {
  for(unsigned i=0;i<neurons.size();i++)
    delete neurons[i];
}

