#ifndef __NET_HPP_
#define __NET_HPP_

#include "layer.hpp"
#include "hiddenlayer.hpp"

class Net {
  public:
    vector<float> input;
    vector<float> output;

    Net(int nInputs);
    ~Net();
    int ReadTS(FILE *fp);
    void addLayer(int nNeurons,int hidden=0);
    void addHiddenLayer(int nNeurons);
    int train(float ratio, float error, float alpha, float momentum, FILE * log);
  void changeWeights(float alpha, float momentum);

  private:
    vector<float> processInput(vector<float> input, int errorcount=0);
    vector< vector<float> > training_set;
    vector<Layer *> layers;
    void randWeights();
};

#endif __NET_HPP_

 