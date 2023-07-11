using UnityEngine;
using System.Collections;
using UnityEngine.Networking;

public class ISSPositionRequest : MonoBehaviour
{
    private string url = "http://api.open-notify.org/iss-now.json";

    IEnumerator Start()
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();

            if (webRequest.result == UnityWebRequest.Result.ConnectionError || webRequest.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.Log("Error: " + webRequest.error);
            }
            else
            {
                // La richiesta è andata a buon fine
                string response = webRequest.downloadHandler.text;
                Debug.Log("Response: " + response);

                // Puoi analizzare la risposta per ottenere la posizione
                // qui puoi fare quello che vuoi con i dati ottenuti
                // Ad esempio, puoi utilizzare una libreria JSON come JsonUtility per analizzare il JSON

                // Esempio di come ottenere la latitudine e la longitudine dalla risposta JSON
                ISSPositionData positionData = JsonUtility.FromJson<ISSPositionData>(response);
                float latitude = float.Parse(positionData.iss_position.latitude);
                float longitude = float.Parse(positionData.iss_position.longitude);

                Debug.Log("Latitude: " + latitude);
                Debug.Log("Longitude: " + longitude);
            }
        }
    }
}

[System.Serializable]
public class ISSPositionData
{
    public ISSPosition iss_position;
}

[System.Serializable]
public class ISSPosition
{
    public string latitude;
    public string longitude;
}