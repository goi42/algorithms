#ifndef MATRIX_H
#define MATRIX_H 1

// Include files
#include <vector>
#include <complex>
#include <iostream>
#include <TMatrixD.h>

//------declare class members------------//
class matrix {
  vector< vector< complex<double> > > content;
  unsigned int Nrows;
  unsigned int Ncols;
public:
  matrix();
  matrix(int,int);
  matrix(int,int,complex<double>);
  matrix(vector< vector< complex<double> > >);
  void DiagonalMatrix(unsigned int,complex<double>);
  void Fill(complex<double>);
  matrix re();
  matrix im();
  matrix transpose();
  complex<double> trace();
  matrix chop(double);
  matrix inverse();
  int GetNrows();
  int GetNrows() const;
  int GetNcols();
  int GetNcols() const;
  void SetNrows(int);
  void SetNcols(int);
  void resize(int,int);
  void print();
  vector< complex<double> > & operator[](int);
  vector< complex<double> > operator[](int) const;
  matrix operator* (const matrix&);
  /* matrix operator* (const complex<double> [] &); */
  matrix operator* (const double&);
  matrix operator* (const double&) const;
  matrix operator* (const complex<double>&);
  matrix operator* (const complex<double>&) const;
  void operator*= (const matrix&);
  void operator*= (const double&);
  void operator*= (const complex<double>&);
  matrix operator+ (const matrix&);
  matrix operator+ (const double&);
  matrix operator+ (const double&) const;
  matrix operator+ (const complex<double>&);
  matrix operator+ (const complex<double>&) const;
  void operator+= (const matrix&);
  void operator+= (const double&);
  void operator+= (const complex<double>&);
  matrix operator- (const matrix&);
  matrix operator- (const double&);
  matrix operator- (const double&) const;
  matrix operator- (const complex<double>&);
  matrix operator- (const complex<double>&) const;
  void operator-= (const matrix&);
  void operator-= (const double&);
  void operator-= (const complex<double>&);
  matrix operator-();//negative of a matrix
};
//-------end class member declarations--------//
//-------define member (and similar) functions--------------//
matrix::matrix(){
}
matrix::matrix(int r,int c){
  this->resize(r,c);
}
matrix::matrix(int r,int c,complex<double>fill){
  this->resize(r,c);
  for(unsigned int i=0; i<Nrows; i++)
    for(unsigned int j=0; j<Ncols; j++)
      content[i][j]=fill;
}
matrix::matrix(vector< vector< complex<double> > > in){
  for(unsigned int i=0; i<in.size(); i++)
    if(i>0&&in[i].size()!=in[i-1].size()){
      cout<<"matrices of class 'matrix' must be rectangular!"<<endl;
      exit(EXIT_FAILURE);
    }
  content = in;
  Nrows = in.size();
  Ncols = in[0].size();
}
void matrix::DiagonalMatrix(unsigned int size,complex<double> fill){
  this->resize(size,size);
  for(unsigned int i=0; i<size; i++)
    for(unsigned int j=0; j<size; j++)
      if(i==j) content[i][j]=fill;
      else     content[i][j]=0;
}
void matrix::Fill(complex<double> fill){
  for(unsigned int i=0; i<Nrows; i++)
    for(unsigned int j=0; j<Ncols; j++)
      content[i][j]=fill;
}
matrix matrix::re(){
  matrix out(Nrows,Ncols);
  for(unsigned int i=0; i<Nrows; i++)
    for(unsigned int j=0; j<Ncols; j++)
      out[i][j]=content[i][j].real();
  return out;
}
matrix matrix::im(){
  matrix out(Nrows,Ncols);
  for(unsigned int i=0; i<Nrows; i++)
    for(unsigned int j=0; j<Ncols; j++)
      out[i][j]=content[i][j].imag();
  return out;
}
matrix matrix::transpose(){
  matrix out(Ncols,Nrows);
  for(unsigned int i=0; i<content.size(); i++)
    for(unsigned int j=0; j<content[i].size(); j++)
      out[i][j]=content[j][i];
  return out;
}
complex<double> matrix::trace(){
  if(Nrows!=Ncols){
    cout<<"The matrix class member 'trace()' is only available for square matrices!"<<endl;
    exit(EXIT_FAILURE);
  }
  complex<double> out=0;
  for(unsigned int i=0; i<content.size(); i++)
    out+=content[i][i];
  return out;
}
matrix matrix::chop(double cutoff = 1e-10){
  matrix out(Nrows,Ncols);
  for(unsigned int i=0; i<Nrows; i++)
    for(unsigned int j=0; j<Ncols; j++)
      if(std::abs(content[i][j].real())<cutoff&&std::abs(content[i][j].imag())<cutoff)
	out[i][j]=complex<double>(0,0);
      else if(std::abs(content[i][j].real())<cutoff)
	out[i][j]=complex<double>(0,content[i][j].imag());
      else if(std::abs(content[i][j].imag())<cutoff)
	out[i][j]=complex<double>(content[i][j].real(),0);
      else out[i][j]=content[i][j];
  return out;
}
void SWAP(matrix &a, int ar, int ac, matrix &b, int br, int bc){
  //non-member function 
  //takes value at a[ar][ac] and replaces it with b[br][bc] and vice-versa
  //hopefully this is what the below gaussj() had in mind...
  complex<double> atemp = a[ar][ac];
  a[ar][ac] = b[br][bc];
  b[br][bc] = atemp;
}
void gaussj(matrix &a, matrix &b){//taken almost verbatim from Numerical Recipes page 44-45
  //non-member function

  //Linear equation solution by Gauss-Jordan elimination.
  //The input matrix is a[0..n-1][0..n-1]. b[0..n-1][0..m-1] is input containing the m right-hand side vectors.
  //On output, a is replaced by its matrix inverse, and b is replaced by the corresponding set of solution vectors.
  int i,icol=0,irow=0,j,k,l,ll,n=a.GetNrows(),m=b.GetNcols();//initialized icol and irow to avoid compiler warnings
  double big;
  complex<double> dum,pivinv;
  vector<int> indxc(n),indxr(n),ipiv(n);//These integer arrays are used for bookkeeping on the pivoting.
  for(j=0;j<n;j++) ipiv[j]=0;
  for(i=0;i<n;i++){//This is the main loop over the columns to be reduced.
    big=0.0;
    for(j=0;j<n;j++)//This is the outer loop of the search for a pivot element
      if(ipiv[j] != 1)
	for(k=0;k<n;k++){
	  if(ipiv[k]==0){
	    if(abs(a[j][k]) >= big){
	      big=abs(a[j][k]);
	      irow=j;
	      icol=k;
	    }
	  }
	}
    ++(ipiv[icol]);
    //We now have the pivot element, so we interchange rows, if needed, to put the pivot element on the diagonal.
    //The columns are not physically interchanged, only relabeled: indxc[i], the column of the (i+1)th pivot element,
    //is the (i=1)th column that is reduced, while indxr[i] is the row in which that pivot element was originally located.
    //If indxr[i] != indxc[i], there is an implied column interchange. With this form of bookkeeping, the solution b's
    //will end up in the correct order, and the inverse matrix will be scrambled by columns.
    if(irow != icol) {
      for(l=0;l<n;l++) SWAP(a,irow,l,a,icol,l);
      for(l=0;l<m;l++) SWAP(b,irow,l,b,icol,l);
    }
    indxr[i]=irow; //We are now ready to divide the pivot row by the pivot element, located at irow and icol
    indxc[i]=icol;
    if(a[icol][icol]==0.0) throw("gaussj: Singular Matrix");
    pivinv=1.0/a[icol][icol];
    a[icol][icol]=1.0;
    for(l=0;l<n;l++) a[icol][l] *= pivinv;
    for(l=0;l<m;l++) b[icol][l] *= pivinv;
    for (ll=0;ll<n;ll++) //Next, we reduce the rows...except for the pivot one, of course
      if(ll != icol){
	dum=a[ll][icol];
	a[ll][icol]=0.0;
	for(l=0;l<n;l++) a[ll][l] -= a[icol][l]*dum;
	for(l=0;l<m;l++) b[ll][l] -= b[icol][l]*dum;
      }
  }
  //This is the end of the main loop over columns of the reduction.
  //It only remains to unscramble the solution in view of the column interchanges.
  //We do this by interchanging pairs of columns in the reverse order that the permutation was built up.
  for(l=n-1;l>=0;l--){
    if(indxr[l] != indxc[l])
      for(k=0;k<n;k++)
	SWAP(a,k,indxr[l],a,k,indxc[l]);
  }//And we are done.
}
void gaussj(matrix &a){//Overloaded version with no right-hand sides. Replaces a by its inverse.
  //non-member function, also taken from NR, see previous function
  matrix b(a.GetNrows(),0);
  gaussj(a,b);
}
matrix matrix::inverse(){
  /* if(Nrows!=Ncols){ */
  /*   cout<<"The matrix class member 'inverse()' is only available for square matrices!"<<endl; */
  /*   exit(EXIT_FAILURE); */
  /* } */
  /* TMatrixD re(Nrows,Ncols); */
  /* TMatrixD im(Nrows,Ncols); */
  /* matrix out; */
  /* bool testre=0;//check if all real parts are 0 */
  /* bool testim=0;//check if all imaginary parts are 0 */
  /* for(unsigned int i=0; i<Nrows; i++)//split real and imaginary components into separate matrices */
  /*   for(unsigned int j=0; j<Ncols; j++){ */
  /*     re[i][j] = real(content[i][j]); */
  /*     im[i][j] = imag(content[i][j]); */
  /*     if(abs(re[i][j])!=0) testre=1;//if any real part is non-zero, testre is true */
  /*     if(abs(im[i][j])!=0) testim=1;//if any imaginary part is non-zero, testim is true */
  /*   } */
  /* if(!testim^!testre){//for purely real or purely imaginary matrices */
  /*   TMatrixD outmat(Nrows,Ncols);//TMatrixD inverse of content */
  /*   TMatrixD *puremat;//pointer to either re or im TMatrixD */
  /*   if     (testre) puremat=&re; */
  /*   else            puremat=&im; */
  /*   outmat = (*puremat).Invert(); */
  /*   out.resize(Nrows,Ncols);//assign out the content of outmat in the appropriate complex field */
  /*   for(unsigned int i=0; i<Nrows; i++){ */
  /*     for(unsigned int j=0; j<Ncols; j++){ */
  /* 	if(testre) out[i][j]=complex<double>(outmat[i][j] , 0            ); */
  /* 	else       out[i][j]=complex<double>(0            , -outmat[i][j]);//C=i*B => C^-1 = -i*B^-1 */
  /*     } */
  /*   } */
  /*   return out; */
  /* }else{//for complex matrices */
  /*   if(re.Determinant()==0||im.Determinant()==0){ */
  /*     cout<<"The matrix class member 'inverse()' works for complex matrices only if they have non-singular real and imaginary parts"<<endl; */
  /*     exit(EXIT_FAILURE); */
  /*   } */
    
  /* } */
  matrix out = (*this);
  gaussj(out);
  return out;
}
int matrix::GetNrows(){
  return Nrows;
}
int matrix::GetNrows() const{
  return Nrows;
}
int matrix::GetNcols(){
  return Ncols;
}
int matrix::GetNcols() const{
  return Ncols;
}
void matrix::SetNrows(int r){
  Nrows = r;
  content.resize(r);
}
void matrix::SetNcols(int c){
  Ncols = c;
  for(unsigned int i=0; i<Nrows; i++)
    content[i].resize(c);
}
void matrix::resize(int r, int c){
  this->SetNrows(r);
  this->SetNcols(c);
}
void matrix::print(){
  for(unsigned int i=0; i<Nrows; i++) for(unsigned int j=0; j<Ncols; j++){
      if(j==0&&i>0)cout<<endl;
      cout<<content[i][j];
    }
  cout<<endl;
}
vector< complex<double> > & matrix::operator[] (int index) {
  return content[index];
}
vector< complex<double> > matrix::operator[] (int index) const{
  return content[index];
}
matrix matrix::operator* (const matrix& param) {
  if(Ncols != param.Nrows){
    cout<<"Requested multiplication of incompatible matrices!"<<endl;
    exit(EXIT_FAILURE);
  }
  matrix temp(Nrows,param.Ncols);
  for(unsigned int i=0; i<Nrows; i++)
    for(unsigned int j=0; j<param.Ncols; j++)
      for(unsigned int k=0; k<Ncols; k++)
	temp[i][j] += content[i][k]*param[k][j];
  return temp;
}
/* matrix matrix::operator* (const complex<double> param[] &) { */
/*   unsigned int arraysize = (sizeof(param)/sizeof(param[0])); */
/*   if(Ncols != arraysize){ */
/*     cout<<"Requested multiplication of incompatible matrices (matrix.Ncols = "<<this->Ncols<<" != N elements in array = "<<arraysize<<")!"<<endl; */
/*     exit(EXIT_FAILURE); */
/*   } */
/*   matrix temp(Nrows,1); */
/*   for(unsigned int i=0; i<Nrows; i++) */
/*     for(unsigned int k=0; k<Ncols; k++) */
/* 	temp[i][0] += content[i][k]*param[k]; */
/*   return temp; */
/* } */
matrix matrix::operator* (const double& param) {
  matrix temp(Nrows,Ncols);
  for(unsigned int i=0; i<Nrows; i++)
    for(unsigned int j=0; j<Ncols; j++)
      temp[i][j] = content[i][j]*param;
  return temp;
}
matrix matrix::operator* (const double& param) const{
  matrix temp(Nrows,Ncols);
  for(unsigned int i=0; i<Nrows; i++)
    for(unsigned int j=0; j<Ncols; j++)
      temp[i][j] = content[i][j]*param;
  return temp;
}
matrix operator* (const double &param, const matrix &matr){
  //non-member function for other-way multiplication
  matrix temp(matr.GetNrows(),matr.GetNcols());
  temp = matr*param;
  return temp;
}
matrix matrix::operator* (const complex<double>& param) {
  matrix temp(Nrows,Ncols);
  for(unsigned int i=0; i<Nrows; i++)
    for(unsigned int j=0; j<Ncols; j++)
      temp[i][j] = content[i][j]*param;
  return temp;
}
matrix matrix::operator* (const complex<double>& param) const{
  matrix temp(Nrows,Ncols);
  for(unsigned int i=0; i<Nrows; i++)
    for(unsigned int j=0; j<Ncols; j++)
      temp[i][j] = content[i][j]*param;
  return temp;
}
matrix operator* (const complex<double> &param, const matrix &matr){
  //non-member function for other-way multiplication
  matrix temp(matr.GetNrows(),matr.GetNcols());
  temp = matr*param;
  return temp;
}
void matrix::operator*= (const matrix& param) {
  (*this) = (*this)*param;
}
void matrix::operator*= (const double& param) {
  (*this) = (*this)*param;
}
void matrix::operator*= (const complex<double>& param) {
  (*this) = (*this)*param;
}
matrix matrix::operator+ (const matrix& param) {
  if(Nrows != param.Nrows || Ncols != param.Ncols){
    cout<<"Requested addition of incompatible matrices!"<<endl;
    exit(EXIT_FAILURE);
  }
  matrix temp(Nrows,Ncols);
  for(unsigned int i=0; i<Nrows; i++)
    for(unsigned int j=0; j<param.Ncols; j++)
      temp[i][j] = content[i][j]+param[i][j];
  return temp;
}
matrix matrix::operator+ (const double& param) {
  matrix temp(Nrows,Ncols);
  for(unsigned int i=0; i<Nrows; i++)
    for(unsigned int j=0; j<Ncols; j++)
      temp[i][j] = content[i][j]+param;
  return temp;
}
matrix matrix::operator+ (const double& param) const{
  matrix temp(Nrows,Ncols);
  for(unsigned int i=0; i<Nrows; i++)
    for(unsigned int j=0; j<Ncols; j++)
      temp[i][j] = content[i][j]+param;
  return temp;
}
matrix operator+ (const double &param, const matrix &matr){
  //non-member function for other-way addition
  matrix temp(matr.GetNrows(),matr.GetNcols());
  temp = matr+param;
  return temp;
}
matrix matrix::operator+ (const complex<double>& param) {
  matrix temp(Nrows,Ncols);
  for(unsigned int i=0; i<Nrows; i++)
    for(unsigned int j=0; j<Ncols; j++)
      temp[i][j] = content[i][j]+param;
  return temp;
}
matrix matrix::operator+ (const complex<double>& param) const{
  matrix temp(Nrows,Ncols);
  for(unsigned int i=0; i<Nrows; i++)
    for(unsigned int j=0; j<Ncols; j++)
      temp[i][j] = content[i][j]+param;
  return temp;
}
matrix operator+ (const complex<double> &param, const matrix &matr){
  //non-member function for other-way addition
  matrix temp(matr.GetNrows(),matr.GetNcols());
  temp = matr+param;
  return temp;
}
void matrix::operator+= (const matrix& param) {
  (*this) = (*this)+param;
}
void matrix::operator+= (const double& param) {
  (*this) = (*this)+param;
}
void matrix::operator+= (const complex<double>& param) {
  (*this) = (*this)+param;
}
matrix matrix::operator- (const matrix& param) {
  return (*this)+(param*(-1));
}
matrix matrix::operator- (const double& param) {
  return (*this)+((-1)*param);
}
matrix matrix::operator- (const double& param) const{
  return (*this)+((-1)*param);
}
matrix operator- (const double &param, const matrix &matr){
  //non-member function for other-way subtraction
  return matr-param;
}
matrix matrix::operator- (const complex<double>& param) {
  return (*this)+((double)(-1)*param);
}
matrix matrix::operator- (const complex<double>& param) const{
  return (*this)+((double)(-1)*param);
}
matrix operator- (const complex<double> &param, const matrix &matr){
  //non-member function for other-way subtraction
  return matr-param;
}
void matrix::operator-= (const matrix& param) {
  (*this) = (*this)-param;
}
void matrix::operator-= (const double& param) {
  (*this) = (*this)-param;
}
void matrix::operator-= (const complex<double>& param) {
  (*this) = (*this)-param;
}
matrix matrix::operator- (){
  return -1*(*this);
}
matrix pow(matrix in,double power){
  //non-member function
  matrix out = in;
  for(int i=1; i<power; i++)
    out*=in;
  return out;
}
matrix sqrt(matrix in){
  //non-member function
  matrix out(in.GetNrows(),in.GetNcols());
  for(int i=0; i<in.GetNrows(); i++)
    for(int j=0; j<in.GetNcols(); j++)
      out[i][j] = sqrt(in[i][j]);
  return out;
}
//------------end define member (and similar) functions------------------//
//------------define/declare non-member functions------------------------//
complex<double> operator* (const double &real, const complex<double> &comp){
  complex<double> temp(real,0);
  complex<double> out = temp*comp;
  return out;
}
complex<double> operator* (const complex<double> &comp, const double &real){
  return real*comp;
}
complex<double> operator/ (const double &real, const complex<double> &comp){
  complex<double> temp(real,0);
  complex<double> out = temp/comp;
  return out;
}
complex<double> operator/ (const complex<double> &comp, const double &real){
  return real/comp;
}
complex<double> operator+ (const double &real, const complex<double> &comp){
  complex<double> temp(real,0);
  complex<double> out = temp+comp;
  return out;
}
complex<double> operator+ (const complex<double> &comp, const double &real){
  return real+comp;
}
complex<double> operator- (const double &real, const complex<double> &comp){
  complex<double> temp(real,0);
  complex<double> out = temp-comp;
  return out;
}
complex<double> operator- (const complex<double> &comp, const double &real){
  return real-comp;
}
//------------end define/declare non-member functions--------------------//
#endif // MATRIX_H
