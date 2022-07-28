import { supabase } from "../../utils/supabase-client"
import {InferGetStaticPropsType} from "next";

const SupabaseTest = ({ cantatas }: InferGetStaticPropsType<typeof getStaticProps>) => {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen py-2">
            {cantatas?.map((cantata) => (
                <p key={cantata.id}>{cantata.title}</p>
            ))}
        </div>
    )
}

export const getStaticProps = async () => {
    const { data: cantatas } = await supabase.from('cantatas').select('*')

    return {
        props: {
            cantatas,
        },
    }
}

export default SupabaseTest
