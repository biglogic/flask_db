# Here is a data.json file where we put some data for pvc , pv and pod i will explain about below

  
  - ``` 
    ns: for namespace for pod and pvc
    kube_service: name of sts or deploy
    pvcname: persistance volume claim name 
    pvname: persistent volume name
    storage: pv volume storage
    storageclaim: pvc claim storage
    storageclassname: name of storage class
    A_zone: availability zone of pv 
    kskind: kubernetes kind name (sts,deploy)
    fstype: file system type
    volumeId: persistent volume id
    replicas: number of replicas
    ```

- this python script will scale down pod 
- create pv and pvc yml 
- delete previous pvc and pv
- apply new pvc and pv from yml 
- scale to given replicas

## Note:-

   - add pvc name as previous one and try to add same pv to the json

