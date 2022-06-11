package bkatwal.zookeeper.demo.model;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;

/** @author "Bikas Katwal" 26/03/19 */


@AllArgsConstructor
@Getter(value = AccessLevel.PUBLIC)
public class FileContents {

  public FileContents()
  {

  }
  
  private String fileName;
  private String contents;
}