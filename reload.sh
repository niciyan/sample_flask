#!/bin/sh

browser-sync start --proxy "http://localhost:5000" --files "app/static" "app/templates"
