package bkatwal.zookeeper.demo.controller;

import static bkatwal.zookeeper.demo.util.ZkDemoUtil.getHostPostOfServer;
import static bkatwal.zookeeper.demo.util.ZkDemoUtil.isEmpty;
import bkatwal.zookeeper.demo.util.FileManager;

import bkatwal.zookeeper.demo.configuration.*;
import bkatwal.zookeeper.demo.model.Models;
import bkatwal.zookeeper.demo.model.FileContents;
import bkatwal.zookeeper.demo.util.ClusterInfo;

import java.util.Arrays;
import java.util.List;
import javax.servlet.http.HttpServletRequest;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.ByteArrayHttpMessageConverter;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import bkatwal.zookeeper.demo.util.FileStorage;

import java.io.IOException;

/** @author "Bikas Katwal" 26/03/19 */
@RestController
public class ZookeeperDemoController {

  private RestTemplate restTemplate = new RestTemplate();

  private boolean amILeader() {
    String leader = ClusterInfo.getClusterInfo().getMaster();
    return getHostPostOfServer().equals(leader);
  }

  @GetMapping("/models")
  public ResponseEntity<List<Models>> getModels() {
    List<Models> models = restTemplate.getForObject(Microservices.ml_microservice_endpoint +Microservices.mlGetAllModels, List.class);
    return ResponseEntity.ok(models);
  }

  @GetMapping("/downloadAllModels")
  public ResponseEntity<byte[]> downloadAllModels()
  {
    String requestUrl = Microservices.ml_microservice_endpoint +Microservices.mlDownloadAllModels;

    FileStorage.deleteDir(getHostPostOfServer());
    FileStorage.createDir(getHostPostOfServer());
      
    RestTemplate rt = new RestTemplate();
    rt.getMessageConverters().add(new ByteArrayHttpMessageConverter());
    HttpHeaders headers = new HttpHeaders();
    headers.setAccept(Arrays.asList(MediaType.APPLICATION_OCTET_STREAM));
    HttpEntity<String> entity = new HttpEntity<String>(headers);
    ResponseEntity<byte[]> response = rt.exchange(requestUrl, HttpMethod.GET, entity, byte[].class, "1");

    FileManager.saveAllModels(response.getBody(), getHostPostOfServer());

    return ResponseEntity.ok(response.getBody());
  }

  @RequestMapping(value = "/updateModel", method = RequestMethod.POST)
  public ResponseEntity<String> updateModel(
    HttpServletRequest request,
    @RequestParam("new_model") MultipartFile multipartFile,
    @RequestParam("model_id") Integer modelID, // prihvatamo u dve promenljive
    @RequestParam("num_of_outputs") Integer numOfInputs
    ) throws IOException
  {
      String requestFrom = request.getHeader("request_from");
      String leader = ClusterInfo.getClusterInfo().getMaster();
      String endpointURL = Microservices.ml_microservice_endpoint +Microservices.mlUpdateModel;

      RestTemplate rt = new RestTemplate();
      rt.getMessageConverters().add(new ByteArrayHttpMessageConverter());

      if (!isEmpty(requestFrom) && requestFrom.equalsIgnoreCase(leader)) // ako je stigao zahtev od lidera, mi treba da sacuvamo taj fajl. Ako zahtev nije stigao od lidera, onda treba da se potrudimo da ode do lidera
        downloadAllModels();
      // saveUpdatedModelLocally(multipartFile, modelID, numOfInputs, endpointURL, rt);

        if (amILeader()) // drigi scenario je ako sam ja bas lider i stigao je zahtev
        {
          saveUpdatedModelLocally(multipartFile, modelID, numOfInputs, endpointURL, rt);
          List<String> liveNodes = ClusterInfo.getClusterInfo().getLiveNodes(); // kojim sve znode-ovima treba da se obratim
        
          for (String node : liveNodes)
          {
            if (getHostPostOfServer().equals(node) == false)
            {
              String requestUrl = "http://".concat(node.concat(Microservices.zkDownloadAllModels));
          
              rt = new RestTemplate();
              rt.getMessageConverters().add(new ByteArrayHttpMessageConverter());
              HttpHeaders headers = new HttpHeaders();
              headers.setAccept(Arrays.asList(MediaType.APPLICATION_OCTET_STREAM));
              HttpEntity<String> entity = new HttpEntity<String>(headers);
              ResponseEntity<byte[]> response = rt.exchange(requestUrl, HttpMethod.GET, entity, byte[].class, "1");
            
              FileManager.saveAllModels(response.getBody(), getHostPostOfServer());
            }
          }
          return ResponseEntity.ok(null);
        }
        else // treci scenario je kada treba da se potrudimo da zahtev ode do lidera
        {
          String requestUrl = "http://".concat(ClusterInfo.getClusterInfo().getMaster().concat(Microservices.zkUpdateModel));
          
          HttpHeaders headers = new HttpHeaders();
          headers.setContentType(MediaType.MULTIPART_FORM_DATA);
          
          MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
          
          body.add("new_model", multipartFile.getResource());
          body.add("model_id", modelID);
          body.add("num_of_outputs", numOfInputs);

          HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
          
          rt.postForEntity(requestUrl, requestEntity, byte[].class);
          
        }
      return ResponseEntity.ok("OK");
  }

  private ResponseEntity<byte[]> saveUpdatedModelLocally(MultipartFile multipartFile, Integer modelID, Integer numOfInputs,
      String endpointURL, RestTemplate rt)
    {
    
    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.MULTIPART_FORM_DATA);
    
    MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
    body.add("new_model", multipartFile.getResource());
    body.add("model_id", modelID);
    body.add("num_of_outputs", numOfInputs);

    HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
    ResponseEntity<byte[]> response = rt.postForEntity(endpointURL, requestEntity, byte[].class);
    FileManager.saveModel(response.getBody(), getHostPostOfServer(), response.getHeaders().get("guid").get(0), response.getHeaders().get("old_model_name").get(0));
    
    return ResponseEntity.ok(response.getBody());
  }

  @RequestMapping(value = "/predict", method = RequestMethod.POST)
  public ResponseEntity<String> predict(
    @RequestParam("dataset") MultipartFile multipartFile,
    @RequestParam("model_id") Integer modelID, // prihvatamo u dve promenljive
    @RequestParam("num_of_outputs") Integer numOfInputs
    ) throws IOException
  {
    String endpointURL = Microservices.ml_microservice_endpoint +Microservices.mlPredict;
    RestTemplate rt = new RestTemplate();
    rt.getMessageConverters().add(new ByteArrayHttpMessageConverter());
    
    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.MULTIPART_FORM_DATA);

    MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
    body.add("dataset", multipartFile.getResource());
    body.add("model_id", modelID);
    body.add("num_of_outputs", numOfInputs);

    HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
    ResponseEntity<String> response = rt.postForEntity(endpointURL, requestEntity, String.class);

    return ResponseEntity.ok(response.getBody());
  }

  @GetMapping("/clusterInfo")
  public ResponseEntity<ClusterInfo> getClusterinfo() {

    return ResponseEntity.ok(ClusterInfo.getClusterInfo());
  }
}
