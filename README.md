# perfdemo
When deploying to K8s you will need a persistent volume configured for your database. Follow these instructions from the google cloud web interface:

Create a new disk that you name ext4 (10GB, standard persistent disk)
Launch a compute engine instance (e.g. ubuntu 14.4)
Attach the disk to the running instance
Open the SSH dialog to the instance
Run command ls /dev/disk/by-id and verify that the disk appears
Run command sudo mkfs.ext4 -F -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/disk/by-id/google-[DISK_NAME] (replace [DISK_NAME] with the name of your disk)
Create a snapshot of the 10GB disk previously created and name it ext4-template
Terminate the compute engine previously launched

Inter application communication
In order for the Django app to communicate with database or the RabbitMQ broker, we need to identify each application somehow. We could assign a static IP to each service and use those, but there's a smarter way to do it. Kuberbetes automatically assigns a DNS names to services so you can access a service without knowing the IP. These DNS names has this format: <name_of_service>.<namespace>.svc.cluster.local. So the database DNS name in our case will always be: postgres-service.default.svc.cluster.local.

You can also retrive the DNS name from an environment variable that has this format: <name_of_service>_SERVICE_HOST. So running this command echo $POSTGRES_SERVICE_SERVICE_HOST in our database container, will yield postgres-service.default.svc.cluster.local.

To get the database host url or (broker host url) in the Django settings file, I first set an environment variable pointing to the name of the host environment variable:

- name: POSTGRES_HOST_ENV_NAME
  value: POSTGRES_SERVICE_SERVICE_HOST

Then I resolve postgres url (DNS name) from the Django settings file this way:

postgres_host_env_name = os.environ['POSTGRES_HOST_ENV_NAME']
postgres_host = os.environ[postgres_host_env_name]

Test comment
