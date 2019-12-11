TITLE sodium_brette_point
 
COMMENT
Sodium conductance point process. 
Based on the publication by Romain Brette "Sharpness of Spike Initiation in Neurons Explained by
Compartmentalization" Plos Computational Biology, 2013.

Author: David Hofmann 2014
Affiliation: Max Planck Institute for Dynamics and Self-Organization, Goettingen
ENDCOMMENT
 
UNITS {
        (mA) = (milliamp)
        (nA) = (nanoamp)
        (mV) = (millivolt)
	(S) = (siemens)
}
 
NEURON {
	POINT_PROCESS NaBrette_point
	USEION na READ ena WRITE ina
        RANGE gnabar, gna, ena, v_resting, trigger
        GLOBAL minf, mtau, v1_2
}

PARAMETER {
        gnabar = 0 (S)	<0,1e9>  : no density as this is a point process
	trigger = 0
	v1_2 = -40 (mV)
	mtau = 0.1 (ms)   : fixed to 100 microsec in Brette 2013
	v_resting = -75 (mV)
}
 
STATE {
        m
}
 
ASSIGNED {
        v (mV)
        ena (mV)

	gna (S)
        ina (nA)
        minf 
}
 
BREAKPOINT {
        SOLVE states METHOD cnexp
        gna = gnabar*m
	ina = gna*(v - ena)
}

INITIAL {
	rates(v)
	m = minf
}

DERIVATIVE states {
        rates(v)
        m' =  (minf-m)/mtau
}
 
PROCEDURE rates(v(mV)) {:Computes rate and other constants at current v.
                        :Call once from HOC to initialize inf at resting v.
        TABLE minf FROM -150 TO 50 WITH 2000

UNITSOFF
	
        minf = 1 / (1 + exp((v1_2 - v)/6))
}
 
NET_RECEIVE (w) {
	trigger = 1
	m = 1 / (1 + exp((v1_2 - v_resting)/6))
}
 
UNITSON
