#!/bin/bash
# Login and get token so we can hit the admin endpoint to trigger the run
token=`curl -d '{"username":"base_admin","password":"'$BASEADMIN_PW'"}' -H "Content-Type: application/json"  -X POST   paws-dp-chart.default.svc.cluster.local/api/user/login | jq  -r '.access_token'`
curl   -H "Content-Type: application/json"  -H "Authorization: Bearer "$token       paws-dp-chart.default.svc.cluster.local/api/admin/user/get_users
