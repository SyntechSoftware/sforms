from django import dispatch

form_was_fullfilled = dispatch.Signal(["form_code", "form_data"])
