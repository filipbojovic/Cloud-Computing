package bkatwal.zookeeper.demo.util;

import org.apache.tomcat.util.http.fileupload.FileUtils;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import bkatwal.zookeeper.demo.configuration.Config;

public class FileManager
{
    public static void zipFile(String path, byte[] data)
    {
        try
        {
            FileOutputStream fos = new FileOutputStream(path);
            fos.write(data);
            fos.close();
        }
        catch (IOException e)
        {
            System.out.println(e.getMessage());
        }
    }
    
    public static void unZipFile(String zipFilePath, String destDir) throws IOException
    {
        byte[] buffer = new byte[1024];
        ZipInputStream zis = new ZipInputStream(new FileInputStream(zipFilePath));
        ZipEntry zipEntry = zis.getNextEntry();
        while (zipEntry != null)
        {
            File newFile = new File(destDir +"/" +zipEntry);
            if (zipEntry.isDirectory())
            {
                if (!newFile.isDirectory() && !newFile.mkdirs())
                    throw new IOException("Failed to create directory " + newFile);
            }
            else
            {
                // fix for Windows-created archives
                File parent = newFile.getParentFile();
                if (!parent.isDirectory() && !parent.mkdirs())
                    throw new IOException("Failed to create directory " + parent);
                
                // write file content
                FileOutputStream fos = new FileOutputStream(newFile);
                int len;
                while ((len = zis.read(buffer)) > 0)
                    fos.write(buffer, 0, len);
                fos.close();
            }
            zipEntry = zis.getNextEntry();
        }

        zis.closeEntry();
        zis.close();

        deleteFile(zipFilePath);
    }

    public static void deleteFile(String filePath)
    {
        File zipToDelete = new File(filePath);
        zipToDelete.delete();
    }

    public static void saveAllModels(byte[] data, String serverHostName)
    {
        String zipPath = Config.zooKeeperRootFolder +serverHostName +Config.zippedFileName;
        String dirPath = Config.zooKeeperRootFolder +serverHostName +"/";

        try
        {
            FileManager.zipFile(zipPath, data); // posto mi stize niz bajtova, napravio sam zip fajl, pa ga onda unzipovao
            FileManager.unZipFile(zipPath, dirPath);
        }
        catch (IOException e)
        {
            System.out.println(e.getMessage());
        }
    }

    public static void saveModel(byte[] data, String serverHostName, String guid, String oldModelName)
    {
        String zipPath = Config.zooKeeperRootFolder +serverHostName +"/" +guid +Config.zippedFileName;
        String dirPath = Config.zooKeeperRootFolder +serverHostName +"/" +guid +"/";
        String oldModelPath = Config.zooKeeperRootFolder +serverHostName +"/" +guid +"/" +oldModelName;

        try
        {
            FileManager.zipFile(zipPath, data);  
            FileManager.unZipFile(zipPath, dirPath);
            FileUtils.forceDelete(new File(oldModelPath));
            FileManager.deleteFile(zipPath);
        }
        catch (IOException e)
        {
            System.out.println(e.getMessage());
        }
    }
}
