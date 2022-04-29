# Main
def main():
    
    while(True):
      
        # Get object name.
        object_name = str(input("Enter an object name: "))
      
        # CALL OBJECT DETECTION FUNCTION
        from object_detection.TFLite_callable_webcam_display import ObjectDetection
        fetch_object_detection = ObjectDetection()
        fetch_object_detection.start(object_name)

        
# Startup
if __name__ == '__main__':

    # Start main program.
    main()
