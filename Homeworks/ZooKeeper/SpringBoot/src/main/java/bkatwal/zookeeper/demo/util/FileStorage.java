package bkatwal.zookeeper.demo.util; // FILE STORAGE pripada ovom paketu

import bkatwal.zookeeper.demo.model.FileContents;
import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

import org.apache.tomcat.util.http.fileupload.FileUtils;

public final class FileStorage
{
    private static String folderPathRoot = "/home/fika/Desktop/git/Cloud-Computing/Homeworks/ZooKeeper/ZK_Models_Storage/";
    public static String folderPath  = "";
    private static List<FileContents> fileList = new ArrayList<>();

    public static void createDir(String folderName)
    {
        folderPath = folderPathRoot +folderName +"/";

        try
        {
            Path path = Paths.get(folderPath);
            Files.createDirectories(path);
            System.out.println("Directory is created!");
        }
        catch (IOException e)
        {
            System.err.println("Failed to create directory!" +e.getMessage());
        }
    }

    public static void deleteDir(String folderName)
    {
        folderPath = folderPathRoot +folderName +"/";

        try
        {
            FileUtils.forceDelete(new File(folderPath));
        }
        catch (IOException e)
        {
            System.out.println("Failed to delete directory " +folderPath +".\n" +e.getMessage());
        }
    }

    public static FileContents GetFile(String fileName)
    {
        String filePath = folderPath +fileName;
        StringBuilder contentBuilder = new StringBuilder();

        try (Stream<String> stream = Files.lines(Paths.get(filePath), StandardCharsets.UTF_8))
        {
            stream.forEach(s -> contentBuilder.append(s).append("\n"));
        }
        catch (IOException e)
        {
            // e.printStrackTrace();
        }

        FileContents fc = new FileContents(fileName, contentBuilder.toString());
        return  fc;
    }

    public static void PutFile(String fileName, String fileContents)
    {
        Path path = Paths.get(folderPath +fileName);
        fileList.add(new FileContents(fileName, fileContents));

        try
        {
            Files.writeString(path, fileContents, StandardCharsets.UTF_8);
        }
        catch (IOException e)
        {

        }
    }

    public static List<String> getFileNames()
    {
        List<String> fileNames = new ArrayList<>();
        File directoryPath = new File(folderPath);
        String contents[] = directoryPath.list();

        for (int i = 0; i < contents.length; i++)
            fileNames.add(contents[i]);
        
        return fileNames;
    }

    public static List<FileContents> getFilesFromStorage()
    {
        return fileList;
    }

    private FileStorage() {}
}