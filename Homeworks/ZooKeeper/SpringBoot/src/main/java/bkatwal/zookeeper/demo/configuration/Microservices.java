package bkatwal.zookeeper.demo.configuration;

public class Microservices {

    private static String ml_microservice_hostname = "http://127.0.0.1";
    private static int ml_microservice_port = 8000;
    public static String ml_microservice_endpoint = ml_microservice_hostname +":" +Integer.toString(ml_microservice_port) +"/";
    
    public static String mlGetAllModels = "getAllModels";
    public static String mlDownloadAllModels = "downloadAllModels";
    public static String mlUpdateModel = "updateModel";
    public static String mlPredict = "predictValues";

    public static String zkDownloadAllModels = "/downloadAllModels";
    public static String zkUpdateModel = "/updateModel";
}
