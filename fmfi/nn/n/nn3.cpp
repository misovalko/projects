#include <stdlib>
#include <algorithm>
#include <vector>
#include <stdio>

#include "net.cpp"
#include "layer.cpp"
#include "neuron.cpp"
#include "hiddenlayer.cpp"
#include "thresholdneuron.cpp"


int main(int argc, char* argv[]) {

  if (argc<2) return 0;
  float ratio, error, alpha, momentum;
  int nNeurons, nInputs, nLayers;
  char filename[256];

  FILE * fp = fopen(argv[1],"rt");
  if (!fp) return 0;

  fscanf(fp, "%s", &filename);
  fscanf(fp, "%f \n %f \n %f \n %f \n %i \n %i",&ratio, &error, &alpha, &momentum, &nInputs, &nLayers);

  Net *parity=new Net(nInputs);

  for(int i=0;i<nLayers;i++) {
    fscanf(fp,"%d\n",&nNeurons);
    if (i!=nLayers-1) parity->addHiddenLayer(nNeurons);
    else parity->addLayer(nNeurons);
  }
  fclose(fp);

  fp = fopen(filename,"rt");
  parity->ReadTS(fp);
  fclose(fp);

  strcpy(filename,argv[1]);
  strcat(filename,".out");
  fp = fopen(filename,"wt");
  randomize();
  parity->train(ratio,error,alpha,momentum,fp);
  fclose(fp);

  delete parity;
  return 1;
}






