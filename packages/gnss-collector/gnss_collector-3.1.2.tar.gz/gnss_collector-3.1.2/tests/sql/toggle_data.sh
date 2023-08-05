#!/bin/env bash
workon collector

function show(){
	code=$1
	echo "Query fro ${code}"
	query=$(sed "s/\[CODE\]/${code}/g" ./show_station.sql)
	PGPASSWORD=${COLLECTOR_DBPASS} psql -U ${COLLECTOR_DBUSER} -d ${COLLECTOR_DBNAME} -c "${query}"
}

function toggle(){
	code=$1
	echo "Antes de cambiar ->"
	show $code
	query=$(sed "s/\[CODE\]/${code}/g" ./toggle_station.sql)
	PGPASSWORD=${COLLECTOR_DBPASS} psql -U ${COLLECTOR_DBUSER} -d ${COLLECTOR_DBNAME} -c "${query}"
	echo "Despues de cambiar->"
	show $code
}


toggle ATJN
