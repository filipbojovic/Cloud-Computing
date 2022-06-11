package bkatwal.zookeeper.demo.model;

import lombok.AllArgsConstructor;
import lombok.Getter;

/** @author "Bikas Katwal" 26/03/19 */
@Getter
@AllArgsConstructor
public class Models {

  private int model_id;
  private String model_name;
  private String dataset_name;
  private double mse;
  private double auc;
  private double acc;
}
