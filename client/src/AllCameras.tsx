// show all the cameras which are there in PC

import React, {useCallback, useEffect, useRef, useState} from "react";

import Webcam from "react-webcam";


const AllCameras = () => {

    const [devices, setDevices] = useState<any[]>([])

    const webcamRef =- useRef(null)

    const [url, setUrl] = useState(null)

    const handleDevices = useCallback((mediaDevices : any) => 
        setDevices(mediaDevices.filter(({ kind } : any ) => kind === "videoinput")), 
        [setDevices]
    )

    React.useEffect(() => {
        navigator.mediaDevices.enumerateDevices().then(handleDevices)
    }, [handleDevices])
    // executes whenver the app loads first time
    // gives a list of devices present on the computer

    const snapshot = useCallback(async() => {
        // const imageSrc = webcamRef.current.getScreenshot()
        // error : Property 'current' does not exist on type 'number'.
        // setUrl(imageSrc)
    }, [webcamRef])

    return (
        <>
        {devices.map((device,key) => (
            <div key={key}>
                <Webcam
                audio={false}
                videoConstraints={{ 
                    width:540,
                    deviceId: device.deviceId }}  
                />
            </div>
        ))}
        </>

    )
}

export default AllCameras;