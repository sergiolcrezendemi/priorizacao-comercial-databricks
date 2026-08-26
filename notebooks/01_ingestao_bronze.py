# Databricks notebook source
# priorizacao-comercial-databricks — Ingestao Bronze
dbutils.widgets.text("catalog", "comercial_dev")
catalog = dbutils.widgets.get("catalog")
# TODO: apontar para a fonte real (ver link da base no README.md)
