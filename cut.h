#ifndef LBJPSIPPI_CUT_H 
#define LBJPSIPPI_CUT_H 1

// Include files
#include <TCut.h>
#include <TString.h>

/** @class cut cut.h LbJpsipPi/cut.h
 *  
 *
 *  @author Michael Wilkinson
 *  @date   2016-01-14
 */
class cut {
public: 
  /// Standard constructor
  cut(TCut);
  cut(TCut,TString);
  //virtual ~cut( ); ///< Destructor
  TCut self;
  TString name;
  int nsig;
  int nbkg;
  int nL;
  int nS;
  int nb;
  
protected:

private:

};
cut::cut(TCut temp){
  self = temp;
}
cut::cut(TCut temp1, TString temp2){
  self = temp1;
  name = temp2;
}

#endif // LBJPSIPPI_CUT_H
