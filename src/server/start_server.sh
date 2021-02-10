echo "Sleeping for 10s..."  
sleep 10;    
echo "Running Alembic";   
alembic upgrade head;   
echo "Starting Flask"  
python -m flask run --host=0.0.0.0