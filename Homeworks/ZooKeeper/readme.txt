java -Dserver.port=8081 -Dzk.url=localhost:2181 -Dleader.algo=2 -jar target/filip-bojovic-ml-zookeeper-1.0-SNAPSHOT.jar
java -Dserver.port=8082 -Dzk.url=localhost:2181 -Dleader.algo=2 -jar target/filip-bojovic-ml-zookeeper-1.0-SNAPSHOT.jar
java -Dserver.port=8083 -Dzk.url=localhost:2181 -Dleader.algo=2 -jar target/filip-bojovic-ml-zookeeper-1.0-SNAPSHOT.jar

http://localhost:8000/docs - ML UI
http://127.0.1.1:8081/swagger-ui.html - ZK UI

- promeniti rootPath u ZK MicroserviceConfiguration.java
- preuzeti ZooKeeper
https://dlcdn.apache.org/zookeeper/zookeeper-3.7.1/apache-zookeeper-3.7.1-bin.tar.gz

