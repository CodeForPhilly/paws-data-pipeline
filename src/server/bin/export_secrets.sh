set -o allexport
 while read k _ v; 
    do 
      eval $k=$v;
      export k;
    done < 'secrets_dict.py'
 set +o allexport