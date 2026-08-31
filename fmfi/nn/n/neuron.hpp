#ifndef __NEURON_HPP_
#define __NEURON_HPP_


#include <vector>

using namespace std;

class Neuron {
  public:
    float output;
    vector<float> input;
    vector<float> weights;

    Neuron(vector<float> input);
    virtual float processInput(vector<float> input, int errorcount);
    void randWeights();
    void changeWeights(float alpha, float momentum, float delta);
  private:
    vector<float> diff;
};

#endif __NEURON_HPP_
