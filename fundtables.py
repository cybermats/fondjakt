#!/usr/bin/python

from peewee import *
import dbconfig


class BaseModel(Model):
	class Meta:
		database = dbconfig.database

class Funds(BaseModel):
	id = PrimaryKeyField()
	name = CharField(null=False)
	currency = CharField(null=False)
	start_date = DateField(null=False)
	end_date = DateField(null=True)

class FundTimeSeries(BaseModel):
	fund = ForeignKeyField(Funds, related_name='time_series')
	date = DateField(null=False)
	value = FloatField(null=False)

	class Meta:
		primary_key = CompositeKey('fund', 'date')

class Index(BaseModel):
	id = PrimaryKeyField()
	name = CharField(null=False)
	start_date = DateField(null=False)
	end_date = DateField(null=True)

class Benchmarks(BaseModel):
	fund = ForeignKeyField(Funds)
	index = ForeignKeyField(Index)
	weight = FloatField(null=False)

	class Meta:
		primary_key = CompositeKey('fund', 'index')


if __name__ == "__main__":
	dbconfig.database.connect()
	if Benchmarks.table_exists():
		Benchmarks.drop_table(fail_silently=True)
	if Index.table_exists():
		Index.drop_table(fail_silently=True)
	if FundTimeSeries.table_exists():
		FundTimeSeries.drop_table(fail_silently=True)
	if Funds.table_exists():
		Funds.drop_table(fail_silently=True)

	Funds.create_table()
	FundTimeSeries.create_table()
	Index.create_table()
	Benchmarks.create_table()

