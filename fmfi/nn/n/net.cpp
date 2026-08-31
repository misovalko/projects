#include "net.hpp"

Net::Net(int nInputs) {
  input.resize(nInputs+1);
  output.resize(input.size());
}

int Net::ReadTS(FILE * fp) {
  float input, output,i ;
  vector<float> pattern(this->input.size()+this->output.size()); // +1 pre desired
  while (!feof(fp)) {
    fscanf(fp," %f | %f ", &input, &output);
    pattern.clear();
    for(unsigned i=0;i<this->input.size()-1;i++) {
      pattern.push_back(((int)input >> (this->input.size()-2-i)) & 1);
    }
    pattern.push_back(-1);
    pattern.push_back(output);
    training_set.push_back(pattern);
  }
  return training_set.size();
}


void Net::addLayer(int nNeurons, int hidden) {
  Layer *v;
  if (hidden) v=(Layer *) new HiddenLayer(output, nNeurons);
  else v=new Layer(output, nNeurons);
  output.resize(v->neurons.size());
  layers.push_back(v);
}

void Net::addHiddenLayer(int nNeurons) {
  this->addLayer(nNeurons, 1);
}


vector<float> Net::processInput(vector<float> input,int errorcount) {
  output=this->input=input;
  for(unsigned i=0;i<layers.size();i++)
    output=layers[i]->processInput(output,errorcount);
  return output;
}


void Net::randWeights() {
  for(unsigned i=0;i<layers.size();i++)
    layers[i]->randWeights();
}


int Net::train(float ratio, float error, float alpha, float momentum, FILE * log) {
  int k=0,m;
  unsigned p; 
  unsigned P=(int )(ratio*training_set.size());
  float d,E,n_output;
  int j,i,test_ok, train_ok;
  vector <float> desired;

  randWeights();
  random_shuffle(training_set.begin(),training_set.end());

  do {
    k++;
    random_shuffle(training_set.begin(),training_set.begin()+P);
    for(p=0;p<P;p++) {
      input.assign(training_set[p].begin(),training_set[p].begin()+this->input.size());
      desired.assign(training_set[p].begin()+this->input.size(),training_set[p].end());
      output=processInput(input,1);

//      printf("\n");
//      for(i=0;i<input.size();i++) printf("%1.0f",input[i]);
//      printf("d: %1.0f o: %.3f",desired[0],output[0]);


      for(i=layers.size()-1;i>=0;i--) {
        layers[i]->delta.clear();
        for(d=0,j=0;j<(signed) layers[i]->neurons.size();j++) {
          if (i==(signed)layers.size()-1) d=(desired[j] - output[j]);
          else
            for(m=0;m<(signed)layers[i+1]->neurons.size();m++)
              d+=layers[i+1]->neurons[m]->weights[j]*layers[i+1]->delta[m];
          layers[i]->delta.push_back(d*layers[i]->neurons[j]->output*(1-layers[i]->neurons[j]->output));
        }
      }

      changeWeights(alpha,momentum);

      output=processInput(input);
//      printf(" n: %.3f",output[0]);

    }
    for(p=0,E=0;p<P;p++) {
      input.assign(training_set[p].begin(),training_set[p].begin()+this->input.size());
      desired.assign(training_set[p].begin()+this->input.size(),training_set[p].end());
      output=processInput(input,1);
        for(j=0;j<(signed) output.size();j++)
          E+=(desired[j]-output[j])*(desired[j]-output[j])/2;
    }

    for(test_ok=0, train_ok=0, p=0;p<training_set.size();p++) {
      input.assign(training_set[p].begin(),training_set[p].begin()+this->input.size());
      desired.assign(training_set[p].begin()+this->input.size(),training_set[p].end());
      output=processInput(input);

      if (output[0]==desired[0])
        if (p<P) train_ok++;
        else test_ok++;
    }
    printf("Epoch: %4d Error: %9.5f, train_ok: %3d/%d, test_ok: %3d/%d\n",k,E, train_ok, P, test_ok, training_set.size()-P);
    fprintf(log, "Epoch: %4d Error: %9.5f, train_ok: %3d/%d, test_ok: %3d/%d\n",k,E, train_ok, P, test_ok, training_set.size()-P);
  } while (E>error);
  return k;
}


Net::~Net() {
  for(unsigned i=0;i<layers.size();i++)
    delete layers[i];
}


void Net::changeWeights(float alpha, float momentum) {
  for(unsigned i=0; i<layers.size();i++)
       layers[i]->changeWeights(alpha,momentum);
}

 