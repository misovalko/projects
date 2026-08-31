#ifndef __HIDDENLAYER_HPP_
#define __HIDDENLAYER_HPP_

#include "layer.hpp"

class HiddenLayer : public Layer {
  public:
    HiddenLayer(vector<float> input, int nNeurons);
};

#endif __HIDDENLAYER_HPP_

 