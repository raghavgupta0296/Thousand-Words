using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Description : MonoBehaviour {

	public Camera centerCamera;
	public GameObject[] painting = new GameObject[7];

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		Vector3 forward = centerCamera.transform.forward * 1000;
        Debug.DrawRay(centerCamera.transform.position, centerCamera.transform.forward, Color.green);


        Vector3 origin = centerCamera.ViewportToWorldPoint(new Vector3(-40.15f, 22.15f, 40.19f));
        RaycastHit hit;
        if (Physics.Raycast(centerCamera.transform.position, centerCamera.transform.forward, out hit, 1000))
        {
        	Debug.Log("hit");
            if (hit.collider.gameObject.layer == 0)
            {
            	Debug.Log("Hit Somethin!");
                foreach (GameObject g in painting)
                {
                    if (hit.collider.gameObject.name.Equals(g.name))
                    {
                    	Debug.Log("Hit g!");
                        hit.collider.gameObject.GetComponent<Expl>().display();
                        Debug.Log("Behold!");
                    }
                }
            }
        }
		
	}
}
