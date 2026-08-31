#ifndef __LAYER_HPP_
#define __LAYER_HPP_

#include "neuron.hpp"

class Layer {
   public:
    vector<Neuron *> neurons;
    vector<float> input;
    vector<float> output;
    vector<float> delta;

    Layer(vector<float> input, int nNeurons);
    ~Layer();
    vector<float> processInput(vector<float> input, int errorcount);
    void randWeights(void);
    void changeWeights(float alpha, float momentum);
};


#endif __LAYER_HPP_

 