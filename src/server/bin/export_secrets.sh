set -o allexport
 while read k _ v; 
    do 
      eval $k=$v;
      export k;
    done < 'secrets.py'
 set +o allexport