#--- function for testing new Discord Bot features - messages will be posted back to #testing channel
def process_test_message(test_message):
    from mydiscord import statuscheck

    status_message = statuscheck()

    return(status_message)      #--- return status message

#--- End - tes function