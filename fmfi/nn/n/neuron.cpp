#include "neuron.hpp"

using namespace std;

Neuron::Neuron(vector<float> input) {
  this->input=input;
  weights.assign(input.size(),0.1);
  diff.assign(input.size(),0);
}

float Neuron::processInput(vector<float> input, int errorcount) {
  float net=0;
  this->input=input;
  for(unsigned i=0;i<input.size();i++)
    net+=weights[i]*input[i];
  output=1/(exp(-net)+1);
  if (!errorcount) {
    if (output>=0.9) output=1;
    else if (output<=0.1) output=0;
  }
  return output;
}


void Neuron::randWeights() {
  weights.clear();
  for(unsigned i=0;i<input.size();i++)
    weights.push_back((float)rand()/RAND_MAX - 0.5);
}


void Neuron::changeWeights(float alpha, float momentum, float delta) {
  for(unsigned i=0;i<weights.size();i++) {
    diff[i]=alpha*delta*input[i] + momentum*diff[i];
    weights[i]+=diff[i];
  }
}
