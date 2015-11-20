double inv_mass(double px_c,double py_c,double pz_c,double pe_c,double px_m,double py_m,double pz_m,double pe_m,double px_n,double py_n,double pz_n,double pe_n) {
  
  TVector3 *_P_Lc = new TVector3();
  TVector3 *_P_Mu = new TVector3();
  TVector3 *_P_Nu = new TVector3();
  
  _P_Lc->SetXYZ(px_c, py_c, pz_c);
  _P_Mu->SetXYZ(px_m, py_m, pz_m);
  _P_Nu->SetXYZ(px_n, py_n, pz_n);
  
  Double_t _E_Lc = pe_c;
  Double_t _E_Mu = pe_m;
  Double_t _E_Nu = pe_n;
  
  TVector3 *_P_W = new TVector3(*_P_Lc + *_P_Mu + *_P_Nu);
  double mass = sqrt( pow((_E_Lc + _E_Mu + _E_Nu),2) - _P_W->Mag2() );
  
  return mass;
  
}
