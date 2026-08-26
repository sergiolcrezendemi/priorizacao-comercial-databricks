# Databricks notebook source
# priorizacao-comercial-databricks — Monitoramento de drift
dbutils.widgets.text("catalog", "comercial_dev")
catalog = dbutils.widgets.get("catalog")
# TODO: configurar Lakehouse Monitoring sobre a tabela Gold de scores
