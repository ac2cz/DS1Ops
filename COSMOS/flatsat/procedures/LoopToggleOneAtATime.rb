loop do
  cmd("EPS_DIST DOMSWITCH with PD_COM1 ENABLE")
  cmd("EPS_DIST DOMSWITCH with PD_COM1 DISABLE")
  
  cmd("EPS_DIST DOMSWITCH with PD_COM2 ENABLE")
  cmd("EPS_DIST DOMSWITCH with PD_COM2 DISABLE")
  
  cmd("EPS_DIST DOMSWITCH with PD_RAHS ENABLE")
   cmd("EPS_DIST DOMSWITCH with PD_RAHS DISABLE")
  
  cmd("EPS_DIST DOMSWITCH with PD_BDOT ENABLE")
  cmd("EPS_DIST DOMSWITCH with PD_BDOT DISABLE")
  
  cmd("EPS_DIST DOMSWITCH with PD_ESTIM ENABLE")
  cmd("EPS_DIST DOMSWITCH with PD_ESTIM DISABLE")
  
  cmd("EPS_DIST DOMSWITCH with PD_WHEELS ENABLE")
  cmd("EPS_DIST DOMSWITCH with PD_WHEELS DISABLE")
    
  cmd("EPS_DIST DOMSWITCH with PD_EPS ENABLE")
  cmd("EPS_DIST DOMSWITCH with PD_EPS DISABLE")
  
  cmd("EPS_DIST DOMSWITCH with PD_PPT ENABLE")
  cmd("EPS_DIST DOMSWITCH with PD_PPT DISABLE")
end
