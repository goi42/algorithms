#ifndef LBJPSIPPI_LAYER_H 
#define LBJPSIPPI_LAYER_H 1

// Include files

/** @class layer layer.h LbJpsipPi/layer.h
 *  
 *
 *  @author Michael Wilkinson
 *  @date   2016-01-15
 */
class layer {
public: 
  /// Standard constructor
  //layer( );
  //virtual ~layer( ); ///< Destructor
  
  TString name; //this is the type of layer
  vector<TString*> element; //this is what each element of the layer is called
  void add_element(TString*);
  int Li = 0; //index indicating which element/comparison of the layer we are on; should be iterated in code
  int nL; //should be set = element.size()
  int nLec; //should be set = element.size() or comparison.size()
  int plL = 1; //products of things in lower levels; should be calculated in code
  int plLx = 1; //products of things in lower levels that are not branches or cuts
  int plLec = 1; //products of things in lower levels using nLec instead of nL
  int plLecx = 1;
  bool compared = kFALSE; //indicates whether this layer is to be drawn on a canvas with other layers
  map<TString*,TString*> comparison;
  void add_comparison(TString*,TString*);
  void add_e_c(TString*,TString*); 
protected:

private:

};
void layer::add_element(TString* temp){
  element.push_back(temp);
}
void layer::add_comparison(TString* key, TString* value){
  comparison.insert( std::pair<TString*,TString*>(key,value) );
}
void layer::add_e_c(TString* key, TString* value){
  add_element(key);
  add_element(value);
  add_comparison(key,value);
}
#endif // LBJPSIPPI_LAYER_H
