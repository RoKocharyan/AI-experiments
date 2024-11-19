import React, { useEffect, useState } from "react";
import { useParams, useLocation } from "react-router-dom";
import GetUsersButton from "./ChangeManager";
import InfoCard from "./InfoCard";
import UserOfClassTable from "./UserOfClassTable";
import { urlPrefix } from "../../../../../../Settings";
import TableView  from "./tableView";
import ChatAssistant from "../../../../ChatAssistant"
import {
  FaEye,
  FaEyeSlash,
  FaCheckCircle,
  FaEllipsisV,
  FaEdit,
  FaTrash,
  FaClock,
} from "react-icons/fa";

const ClassView = () => {
  const { id } = useParams();
  const location = useLocation();
  const [classData, setClassData] = useState(location.state?.classItem || null);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(!classData);
  const [customization, setCustomization] = useState(null);
  const [accountManager, setAccountManager] = useState(null);

  useEffect(() => {
    //console.log("classData:", classData);

    if (classData) {
      fetchUserData();
      fetchAccountCustomization();
    }
  }, [id, classData]);

  const fetchAccountCustomization = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      console.error("No token found");
      return;
    }

    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };

    try {
      const url = `http://localhost:8080/account/${classData.id}`;
      const response = await fetch(url, requestOptions);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setCustomization(data.account);
      
    } catch (error) {
      console.error("Error fetching customization data:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchUserData = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      console.error("No token found");
      return;
    }

    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };

    try {
      setLoading(true);
      const url = `${urlPrefix}/Account/users?accountId=${classData.id}`;
      const response = await fetch(url, requestOptions);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const manager = data.find((user) => user.accountRoleId === 2);
      setAccountManager(manager || {});
      setUsers(data);
    } catch (error) {
      console.error("Error fetching user data:", error);
    } finally {
      setLoading(false);
    }
  };

  const roleMap = {
    1: 'SysAdmin',
    2: 'Admin',
    4: 'AccountManager',
    8: 'Beneficiary',
  };
  
  const userColumns = [
    {
      label: 'Image',
      key: 'userImage',
      render: (row) => (
        <img
          src={row.userImage || 'default-photo-url'}
          alt={`${row.firstName} ${row.lastName}`}
          className="w-10 h-10 rounded-full"
        />
      ),
    },
    {
      label: 'Name',
      key: 'name',
      render: (row) => `${row.firstName} ${row.lastName}`,
    },
    {
      label: 'Role',
      key: 'accountRoleId',
      render: (row) => roleMap[row.accountRoleId] || 'Unknown',
    },
    // { label: 'Email', key: 'email' },
    // {
    //   label: 'Created Date',
    //   key: 'createDate',
    //   render: (row) => new Date(row.createDate).toLocaleDateString(),
    // },
  ];
  if (loading) {
    return <div>Loading...</div>;
  }

  if (!classData) {
    return <div>Class data not found</div>;
  }

  return (
    <main className="p-6 min-w-full bg-[#FFFFFF] border border-[#D1D5DB] shadow-md rounded-lg">
      <div className="mb-6 text-black">
        <div className="flex min-w-full justify-between items-center border-b-2 border-gray-200 pb-2">
          <h1 className="text-4xl font-bold">{classData.name}</h1>
          <div className="flex items-center text-lg font-semibold text-[#000000]">
            <span className="mx-2">
              {classData.statusId === 2 ? "Active" : "Pending"}
            </span>
            {classData.statusId === 2 ? (
              <FaCheckCircle className="text-[#00f100] mx-2" />
            ) : (
              <FaClock className="text-[#ffde23] mx-2" />
            )}
          </div>
        </div>
        <div className="py-2 flex min-w-full justify-between items-center">
          <h1 className="text-2xl border-gray-200 pb-2">
            {classData.description}
          </h1>
          <div className="flex items-center text-lg font-semibold text-[#000000]">
            <span className="mx-2">
              {classData.isVisible ? "Visible" : "Invisible"}
            </span>
            {classData.isVisible ? (
              <FaEye className="text-[#21fb00] mx-2" />
            ) : (
              <FaEyeSlash className="text-[#ff0000] mx-2" />
            )}
          </div>
        </div>
        <div className="grid grid-cols-3 gap-6">
          <InfoCard headline="User count" info={users.length} />
          <InfoCard
            headline="Account Manager"
            img={
              accountManager?.userImage ||
              "https://png.pngtree.com/png-vector/20220309/ourmid/pngtree-not-allowed-man-forbid-user-profile-vector-png-image_35657800.png"
            }
            info={`${accountManager?.firstName || ""} ${
              accountManager?.lastName || ""
            }`}
          >
            <GetUsersButton userList={users} />
          </InfoCard>
          <InfoCard headline="Onboarding Link" link={customization?.url} />
          
        </div>
      </div>

      {/* <UserOfClassTable users={users} /> */}
      <TableView data={users} columns={userColumns}/>
      <ChatAssistant/>
    </main>
  );
};

export default ClassView;
