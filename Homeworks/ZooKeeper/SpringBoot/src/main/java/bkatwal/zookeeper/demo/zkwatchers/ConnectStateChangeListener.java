package bkatwal.zookeeper.demo.zkwatchers;

import static bkatwal.zookeeper.demo.util.ZkDemoUtil.getHostPostOfServer;
import static bkatwal.zookeeper.demo.util.ZkDemoUtil.isEmpty;

import bkatwal.zookeeper.demo.api.ZkService;
import bkatwal.zookeeper.demo.configuration.Microservices;
import bkatwal.zookeeper.demo.util.ClusterInfo;
import bkatwal.zookeeper.demo.util.FileManager;

import java.util.Arrays;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;
import org.I0Itec.zkclient.IZkStateListener;
import org.apache.zookeeper.Watcher.Event.KeeperState;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.ByteArrayHttpMessageConverter;
import org.springframework.web.client.RestTemplate;

/** @author "Bikas Katwal" 02/04/19 */
@Slf4j
@Setter
public class ConnectStateChangeListener implements IZkStateListener {

  private ZkService zkService;
  private RestTemplate restTemplate = new RestTemplate();

  @Override
  public void handleStateChanged(KeeperState state) throws Exception {
    log.info(state.name()); // 1. disconnected, 2. expired, 3. SyncConnected
  }

  @Override
  public void handleNewSession() throws Exception {
    log.info("connected to zookeeper");

    // sync data from master
    syncDataFromMaster(); // kada se ukljuci novi node - hajde da sinhronizujemo podatke sa mastera. Ova metoda je izvrsena kada se startuje novi node.

    // add new znode to /live_nodes to make it live
    zkService.addToLiveNodes(getHostPostOfServer(), "cluster node");
    ClusterInfo.getClusterInfo().getLiveNodes().clear();
    ClusterInfo.getClusterInfo().getLiveNodes().addAll(zkService.getLiveNodes());

    // re try creating znode under /election
    // this is needed, if there is only one server in cluster
    String leaderElectionAlgo = System.getProperty("leader.algo");
    if (isEmpty(leaderElectionAlgo) || "2".equals(leaderElectionAlgo)) {
      zkService.createNodeInElectionZnode(getHostPostOfServer());
      ClusterInfo.getClusterInfo().setMaster(zkService.getLeaderNodeData2());
    } else {
      if (!zkService.masterExists()) {
        zkService.electForMaster();
      } else {
        ClusterInfo.getClusterInfo().setMaster(zkService.getLeaderNodeData());
      }
    }
  }

  @Override
  public void handleSessionEstablishmentError(Throwable error) throws Exception {
    log.info("could not establish session");
  }

  private void syncDataFromMaster() {
    // BKTODO need try catch here for session not found
    if (getHostPostOfServer().equals(ClusterInfo.getClusterInfo().getMaster())) {
      return;
    }

    String requestUrl = "http://".concat(ClusterInfo.getClusterInfo().getMaster().concat(Microservices.zkDownloadAllModels));
    RestTemplate rt = new RestTemplate();
    rt.getMessageConverters().add(new ByteArrayHttpMessageConverter());
    HttpHeaders headers = new HttpHeaders();
    headers.setAccept(Arrays.asList(MediaType.APPLICATION_OCTET_STREAM));
    HttpEntity<String> entity = new HttpEntity<String>(headers);
    ResponseEntity<byte[]> response = rt.exchange(requestUrl, HttpMethod.GET, entity, byte[].class, "1");
  
    FileManager.saveAllModels(response.getBody(), getHostPostOfServer());
  }
}
