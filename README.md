# UpdateDocxService

UpdateDocxService 是一个用于上传、更新和下载 DOCX 文件目录的服务。它设计用于异步处理多个文件上传，确保高效处理。

## Project Structure

```
UpdateDocxService
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── services
│   │   ├── __init__.py
│   │   └── toc_updater.py
│   ├── routes
│   │   ├── __init__.py
│   │   └── docx_routes.py
│   └── utils
│       ├── __init__.py
│       └── file_handler.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Features

- 上传 DOCX 文件并更新其目录。
- 通过 UUID 下载更新后的文件。
- 删除上传的文件。

## Setup Instructions

1. Clone the repository:

   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:

   ```
   cd UpdateDocxService
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python src/main.py
   ```
5. **<span style="color:red"> Run the application with start_service.bat:</span>**

```
./start_service.bat
```

使用 start_service.bat 启动时，请在要目录下添加一个 test.docx 空文件

## API Endpoints

### 上传文件

#### POST /api/upload-docx/

请求参数：

- `file`: 要上传的 DOCX 文件。

响应：

- `uuid`: 上传文件的唯一标识符。

### 读取更新后的文件

#### GET /api/download-docx/{uuid}

请求参数：

- `uuid`: 上传文件的唯一标识符。

响应：

- 更新后的 DOCX 文件。

### 删除文件

#### DELETE /api/delete-docx/{uuid}

请求参数：

- `uuid`: 上传文件的唯一标识符。

响应：

- 删除成功的消息。

# 调用示例

以下是一个使用 Java 调用该服务的示例代码：

```java
// filepath: /path/to/README.md
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class UploadDocxExample {
    public static void main(String[] args) {
        String urlString = "http://localhost:8000/upload-docx/";
        String filePath = "path/to/your/file.docx";

        try {
            File file = new File(filePath);
            FileInputStream fileInputStream = new FileInputStream(file);
            URL url = new URL(urlString);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setDoOutput(true);
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "multipart/form-data; boundary=---ContentBoundary");

            OutputStream outputStream = connection.getOutputStream();
            outputStream.write(("-----ContentBoundary\r\n" +
                    "Content-Disposition: form-data; name=\"file\"; filename=\"" + file.getName() + "\"\r\n" +
                    "Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document\r\n\r\n").getBytes());

            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = fileInputStream.read(buffer)) != -1) {
                outputStream.write(buffer, 0, bytesRead);
            }

            outputStream.write("\r\n-----ContentBoundary--\r\n".getBytes());
            outputStream.flush();
            outputStream.close();
            fileInputStream.close();

            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                System.out.println("文件上传成功");
            } else {
                System.out.println("文件上传失败，响应码：" + responseCode);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

## 使用 Java 和 docx4j 生成并上传.docx 文件

以下是一个使用 Java 和 docx4j 生成.docx 文档并直接调用该服务的示例代码：

```java
// filepath: /e:/temp/UpdateDocxService/README.md
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

import org.docx4j.openpackaging.packages.WordprocessingMLPackage;
import org.docx4j.wml.ObjectFactory;
import org.docx4j.wml.P;

public class UploadDocxExample {
    public static void main(String[] args) {
        try {
            // 创建一个新的WordprocessingMLPackage
            WordprocessingMLPackage wordMLPackage = WordprocessingMLPackage.createPackage();
            ObjectFactory factory = new ObjectFactory();

            // 创建一个段落并添加到文档中
            P paragraph = factory.createP();
            paragraph.getContent().add(factory.createR().getContent().add(factory.createText("Hello, World!")));
            wordMLPackage.getMainDocumentPart().addObject(paragraph);

            // 将文档内容写入ByteArrayOutputStream
            ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
            wordMLPackage.save(byteArrayOutputStream);

            // 调用上传服务
            String urlString = "http://localhost:8000/api/upload-docx/";
            URL url = new URL(urlString);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setDoOutput(true);
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "multipart/form-data; boundary=---ContentBoundary");

            OutputStream outputStream = connection.getOutputStream();
            outputStream.write(("-----ContentBoundary\r\n" +
                    "Content-Disposition: form-data; name=\"file\"; filename=\"generated.docx\"\r\n" +
                    "Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document\r\n\r\n").getBytes());

            byteArrayOutputStream.writeTo(outputStream);

            outputStream.write("\r\n-----ContentBoundary--\r\n".getBytes());
            outputStream.flush();
            outputStream.close();
            byteArrayOutputStream.close();

            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                System.out.println("文件上传成功");
            } else {
                System.out.println("文件上传失败，响应码：" + responseCode);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

## 使用 Java 调用 UpdateDocxService

以下是一个使用 Java 调用 UpdateDocxService 的示例程序，包括上传、读取和删除文件的过程：

```java
// filepath: /e:/temp/UpdateDocxService/README.md
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

import org.docx4j.openpackaging.packages.WordprocessingMLPackage;
import org.docx4j.wml.ObjectFactory;
import org.docx4j.wml.P;

public class UpdateDocxServiceExample {
    public static void main(String[] args) {
        String uploadUrl = "http://localhost:8000/api/upload-docx/";
        String downloadUrl = "http://localhost:8000/api/download-docx/";
        String deleteUrl = "http://localhost:8000/api/delete-docx/";
        String filePath = "E:/temp/test-docx/sample.docx";
        String downloadDir = "E:/temp/download-docx/";

        try {
            // Step 1: 上传文件
            String uuid = uploadFile(uploadUrl, filePath);
            System.out.println("Uploaded file UUID: " + uuid);

            // Step 2: 读取文件
            downloadFile(downloadUrl, uuid, downloadDir + "sample.docx");

            // Step 3: 删除文件
            deleteFile(deleteUrl, uuid);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static String uploadFile(String uploadUrl, String filePath) throws IOException {
        File file = new File(filePath);
        FileInputStream fileInputStream = new FileInputStream(file);
        URL url = new URL(uploadUrl);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setDoOutput(true);
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Content-Type", "multipart/form-data; boundary=---ContentBoundary");

        OutputStream outputStream = connection.getOutputStream();
        outputStream.write(("-----ContentBoundary\r\n" +
                "Content-Disposition: form-data; name=\"file\"; filename=\"" + file.getName() + "\"\r\n" +
                "Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document\r\n\r\n").getBytes());

        byte[] buffer = new byte[4096];
        int bytesRead;
        while ((bytesRead = fileInputStream.read(buffer)) != -1) {
            outputStream.write(buffer, 0, bytesRead);
        }

        outputStream.write("\r\n-----ContentBoundary--\r\n".getBytes());
        outputStream.flush();
        outputStream.close();
        fileInputStream.close();

        int responseCode = connection.getResponseCode();
        if (responseCode == HttpURLConnection.HTTP_OK) {
            Scanner scanner = new Scanner(connection.getInputStream());
            String responseBody = scanner.useDelimiter("\\A").next();
            scanner.close();
            return responseBody.split(":")[1].replaceAll("[\"{}]", "").trim();
        } else {
            throw new IOException("Failed to upload file, response code: " + responseCode);
        }
    }

    private static void downloadFile(String downloadUrl, String uuid, String outputPath) throws IOException {
        URL url = new URL(downloadUrl + uuid);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");

        int responseCode = connection.getResponseCode();
        if (responseCode == HttpURLConnection.HTTP_OK) {
            try (FileOutputStream fileOutputStream = new FileOutputStream(outputPath)) {
                byte[] buffer = new byte[4096];
                int bytesRead;
                while ((bytesRead = connection.getInputStream().read(buffer)) != -1) {
                    fileOutputStream.write(buffer, 0, bytesRead);
                }
            }
            System.out.println("Downloaded file to: " + outputPath);
        } else {
            throw new IOException("Failed to download file, response code: " + responseCode);
        }
    }

    private static void deleteFile(String deleteUrl, String uuid) throws IOException {
        URL url = new URL(deleteUrl + uuid);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("DELETE");

        int responseCode = connection.getResponseCode();
        if (responseCode == HttpURLConnection.HTTP_OK) {
            System.out.println("Deleted file with UUID: " + uuid);
        } else {
            throw new IOException("Failed to delete file, response code: " + responseCode);
        }
    }
}
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
